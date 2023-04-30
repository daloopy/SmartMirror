
#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_log.h"
#include "driver/uart.h"
#include "string.h"
#include "driver/gpio.h"
#include "freertos/timers.h"
#include "freertos/queue.h"
#include "sdkconfig.h"
#include "driver/rmt.h"
#include "driver/rmt_tx.h"
#include "led_strip_encoder.h"
#include <string.h>
#include <stdlib.h>
#include <iconv.h>


#define RMT_LED_STRIP_RESOLUTION_HZ 10000000 // 10MHz resolution, 1 tick = 0.1us (led strip needs a high resolution)
#define RMT_LED_STRIP_GPIO_NUM      20

#define EXAMPLE_LED_NUMBERS         60
#define EXAMPLE_CHASE_SPEED_MS      100

static const char *TAG = "example";

static uint8_t led_strip_pixels[EXAMPLE_LED_NUMBERS * 3];


static const int RX_BUF_SIZE = 1024;

#define TXD_PIN (GPIO_NUM_17)
#define RXD_PIN (GPIO_NUM_18)

#define GPIO_INPUT_IO_4     4
#define GPIO_INPUT_PIN_SEL  (1ULL<<GPIO_INPUT_IO_4)

#define UART UART_NUM_1


void led_set_color(uint32_t r, uint32_t g, uint32_t b) {

    ESP_LOGI(TAG, "Create RMT TX channel");
    rmt_channel_handle_t led_chan = NULL;
    rmt_tx_channel_config_t tx_chan_config = {
        .clk_src = RMT_CLK_SRC_DEFAULT, // select source clock
        .gpio_num = RMT_LED_STRIP_GPIO_NUM,
        .mem_block_symbols = 64, // increase the block size can make the LED less flickering
        .resolution_hz = RMT_LED_STRIP_RESOLUTION_HZ,
        .trans_queue_depth = 4, // set the number of transactions that can be pending in the background
    };
    ESP_ERROR_CHECK(rmt_new_tx_channel(&tx_chan_config, &led_chan));

    ESP_LOGI(TAG, "Install led strip encoder");
    rmt_encoder_handle_t led_encoder = NULL;
    led_strip_encoder_config_t encoder_config = {
        .resolution = RMT_LED_STRIP_RESOLUTION_HZ,
    };
    ESP_ERROR_CHECK(rmt_new_led_strip_encoder(&encoder_config, &led_encoder));

    ESP_LOGI(TAG, "Enable RMT TX channel");
    ESP_ERROR_CHECK(rmt_enable(led_chan));

    // Set all the LEDs to the same color
    for (int i = 0; i < EXAMPLE_LED_NUMBERS; i++) {
        led_strip_pixels[i * 3 + 0] = g;
        led_strip_pixels[i * 3 + 1] = r;
        led_strip_pixels[i * 3 + 2] = b;
    }

    // Flush RGB values to LEDs
    rmt_transmit_config_t tx_config = {
        .loop_count = 0, // no transfer loop
    };
    for(int i = 0; i < 100; i ++){
        ESP_ERROR_CHECK(rmt_transmit(led_chan, led_encoder, led_strip_pixels, sizeof(led_strip_pixels), &tx_config));
    }
}


void led_set_static_color() {
    // Set all the LEDs to the same color
    uint32_t r = 255; //blue
    uint32_t g = 255; //half blue or red
    uint32_t b = 255;
    led_set_color(r, g, b);
}

void led_set_red() {
    // Set all the LEDs to the same color
    uint32_t r = 255; //blue
    uint32_t g = 0; //half blue or red
    uint32_t b = 0;
    led_set_color(r, g, b);
}

void led_turnoff(){
    uint32_t r = 0; //blue
    uint32_t g = 0; //half blue or red
    uint32_t b = 0;
    led_set_color(r, g, b);
}

void init(void) {
    const uart_config_t uart_config = {
        .baud_rate = 115200,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_APB,
    };
    // We won't use a buffer for sending data.
    uart_driver_install(UART, RX_BUF_SIZE * 2, 0, 0, NULL, 0);
    uart_param_config(UART, &uart_config);
    uart_set_pin(UART, TXD_PIN, RXD_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
}

int sendData(const char* logName, const char* data)
{
    const int len = strlen(data);
    const int txBytes = uart_write_bytes(UART, data, len);
    ESP_LOGI(logName, "Wrote %d bytes", txBytes);
    printf("Wrote %d bytes",txBytes);

    return txBytes;
}

static void tx_task(void *arg)
{
    static const char *TX_TASK_TAG = "TX_TASK";
    esp_log_level_set(TX_TASK_TAG, ESP_LOG_INFO);
    //int gpio_level = *((int *)arg);
    int gpio_level = gpio_get_level(GPIO_INPUT_IO_4);
    char buffer[17];
    sprintf(buffer, "GPIO4_value: %d \n", gpio_level);
    //printf("sending value");
    while (1) {
        uart_write_bytes(UART, buffer, sizeof(buffer));
        vTaskDelay(2000 / portTICK_PERIOD_MS);
        vTaskDelete(NULL);
    }
}

// static void tx_task(void *arg)
// {
//     static const char *TX_TASK_TAG = "TX_TASK";
//     esp_log_level_set(TX_TASK_TAG, ESP_LOG_INFO);
//     //int gpio_level = *((int *)arg);
//     int gpio_level = gpio_get_level(GPIO_INPUT_IO_4);
//     char buffer[17];
//     sprintf(buffer, "GPIO4_value: %d \n", gpio_level);

//     // Convert buffer to a string object
//     char *str_buffer = malloc(strlen(buffer) + 1);
//     strcpy(str_buffer, buffer);

//     // Encode the string using iconv
//     char *inbuf = str_buffer;
//     char *outbuf = malloc(strlen(buffer) * 2); // allocate space for worst-case scenario (every byte gets encoded as 2)
//     size_t inbytesleft = strlen(buffer);
//     size_t outbytesleft = strlen(buffer) * 2;
//     iconv_t cd = iconv_open("ISO-8859-1", "UTF-8");
//     iconv(cd, &inbuf, &inbytesleft, &outbuf, &outbytesleft);
//     iconv_close(cd);

//     // Strip the string of any leading or trailing whitespace
//     char *start = outbuf;
//     while (*start == ' ' || *start == '\t' || *start == '\n' || *start == '\r') {
//         start++;
//     }
//     char *end = outbuf + strlen(outbuf) - 1;
//     while (end > start && (*end == ' ' || *end == '\t' || *end == '\n' || *end == '\r')) {
//         end--;
//     }
//     *(end + 1) = '\0';

//     // Send the encoded and stripped string over UART
//     while (1) {
//         uart_write_bytes(UART, outbuf, strlen(outbuf));
//         vTaskDelay(2000 / portTICK_PERIOD_MS);
//         free(outbuf);
//         free(str_buffer);
            

//         // Delete the task when it's done
//         vTaskDelete(NULL);
//     }

//     // Free the dynamically allocated memory for the strings

// }

void setup_gpio() {
    // Configure GPIO4 as input
    gpio_config_t io_conf;
    io_conf.intr_type = GPIO_INTR_DISABLE;
    io_conf.mode = GPIO_MODE_INPUT;
    io_conf.pin_bit_mask = GPIO_INPUT_PIN_SEL;
    io_conf.pull_down_en = 0;
    io_conf.pull_up_en = 1;
    gpio_config(&io_conf);
}

static void timer_callback(TimerHandle_t xTimer) {
    int gpio_level = gpio_get_level(GPIO_INPUT_IO_4);
    xTaskCreate(tx_task, "uart_tx_task", 1024*2,(void *)&gpio_level, configMAX_PRIORITIES-1, NULL);
}

void app_main(void)
{
    setup_gpio();
    init();
    TimerHandle_t timer = xTimerCreate("GPIO4_Timer", pdMS_TO_TICKS(2000), pdTRUE, 0, timer_callback);
    xTimerStart(timer, 0);
    led_set_static_color();
}


// #include "freertos/FreeRTOS.h"
// #include "freertos/task.h"
// #include "esp_system.h"
// #include "esp_log.h"
// #include "driver/uart.h"
// #include "string.h"
// #include "driver/gpio.h"

// static const int RX_BUF_SIZE = 1024;

// #define TXD_PIN (GPIO_NUM_43)
// #define RXD_PIN (GPIO_NUM_44)

// #define UART UART_NUM_0

// void init(void) {
//     const uart_config_t uart_config = {
//         .baud_rate = 115200,
//         .data_bits = UART_DATA_8_BITS,
//         .parity = UART_PARITY_DISABLE,
//         .stop_bits = UART_STOP_BITS_1,
//         .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
//         .source_clk = UART_SCLK_APB,
//     };
//     // We won't use a buffer for sending data.
//     uart_driver_install(UART, RX_BUF_SIZE * 2, 0, 0, NULL, 0);
//     uart_param_config(UART, &uart_config);
//     uart_set_pin(UART, TXD_PIN, RXD_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
// }

// int sendData(const char* logName, const char* data)
// {
//     const int len = strlen(data);
//     const int txBytes = uart_write_bytes(UART, data, len);
//     ESP_LOGI(logName, "Wrote %d bytes", txBytes);
//     return txBytes;
// }

// static void tx_task(void *arg)
// {
//     static const char *TX_TASK_TAG = "TX_TASK";
//     esp_log_level_set(TX_TASK_TAG, ESP_LOG_INFO);
//     while (1) {
//         uart_write_bytes(UART, "Hello \n", 7);
//         vTaskDelay(2000 / portTICK_PERIOD_MS);
//     }
// }


// static void rx_task(void *arg)
// {
//     static const char *RX_TASK_TAG = "RX_TASK";
//     esp_log_level_set(RX_TASK_TAG, ESP_LOG_INFO);

//     //uint8_t* data = (uint8_t*) malloc(RX_BUF_SIZE+1);
//     uint8_t* data = (uint8_t*) malloc(RX_BUF_SIZE);
//     while (1) {
//         const int rxBytes = uart_read_bytes(UART, data, RX_BUF_SIZE, 500 / portTICK_PERIOD_MS);
//         if (rxBytes > 0) {
//             data[rxBytes] = '\0';
//             ESP_LOGI(RX_TASK_TAG, "Read %d bytes: '%s'", rxBytes, data);
//             // ESP_LOG_BUFFER_HEXDUMP(RX_TASK_TAG, data, rxBytes, ESP_LOG_INFO);
//         }
//     }
//     free(data);
// }

// void app_main(void)
// {
//     init();
//     //xTaskCreate(rx_task, "uart_rx_task", 1024*2, NULL, configMAX_PRIORITIES, NULL);
//     xTaskCreate(tx_task, "uart_tx_task", 1024*2, NULL, configMAX_PRIORITIES-1, NULL);
// }