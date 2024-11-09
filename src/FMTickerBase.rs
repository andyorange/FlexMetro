use std::sync::{Arc, Mutex};
use std::thread;
use flet::{Page, UserControl, Stack, colors};

enum FMTickPositions {
    T_none,
    T_section,
    T_rest,
}

struct FMSectionTimer {
    tick_end_callback: Arc<Mutex<Option<Box<dyn Fn() -> ()>>>>,
}

impl FMSectionTimer {
    fn add_tick_end_callback(&self, callback: Box<dyn Fn() -> ()>) {
        let mut callback_guard = self.tick_end_callback.lock().unwrap();
        *callback_guard = Some(callback);
    }
}


// -------


trait FMTickerBase {
    fn connect_timer(&mut self);
    fn update(&mut self);
    fn render(&self) -> Stack;
}

// -------

trait FMTickerBase {
    fn tick_callback(&mut self, section_info: FMBarElement, cnt: i32, ignore_subbeats: Option<bool>);
    fn fix_subbeat(&mut self, tick_value: i32, ignore_subbeats: Option<bool>);
}

impl FMTickerBase for FMCircleTicker {
    fn connect_timer(&mut self) {
        if let Some(timer) = &self.timer {
            let callback = Box::new(move || {
                self.state = FMTickPositions::T_none;
                self.update();
            });
            timer.add_tick_end_callback(callback);
        }
    }

    fn update(&mut self) {
        // Implement the logic to update the UI based on the current state
    }

    fn render(&self) -> Stack {
        // Implement the logic to render the UI based on the current state
        let controls = vec![];
        Stack::new(controls)
    }
}
