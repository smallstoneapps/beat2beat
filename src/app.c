#include <pebble.h>


static Window* s_window;


static void prv_init(void);
static void prv_deinit(void);


int main(void) {
  prv_init();
  app_event_loop();
  prv_deinit();
}

static void prv_init(void) {
  s_window = window_create();
  window_stack_push(s_window, false);
}

static void prv_deinit(void) {

}
