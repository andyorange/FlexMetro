use std::sync::{Arc, Mutex};
use std::thread;
use flet::{Page, UserControl, Stack, colors};
use crate::FMTickerBase;


struct FMCircleTicker {
    timer: Option<FMSectionTimer>,
    page: Page,
    state: FMTickPositions,
    cwidth: f64,
    cheight: f64,
    base_diameter: f64,
    diam: [f64; 3],
    circle_cols_bg: [&'static str; 3]
}


use flutter_engine::{FlutterEngine, ChannelMessage, ChannelMessageResponse};

impl FMTickerBase for FMCircleTicker {
    fn tick_callback(&mut self, section_info: FMBarElement, cnt: i32, ignore_subbeats: Option<bool>) {
        // Access the class variables using self
        let cwidth = self.cwidth;
        let cheight = self.cheight;

        // Create a FlutterEngine instance
        let mut engine = FlutterEngine::new();

        // Load the Flutter app
        engine.load_app("./FMUICircles.dart").unwrap();

        // Create a ChannelMessage to send to Flutter
        let message = ChannelMessage::new(
            "tick_callback",
            format!("{:?}, {}, {:?}", section_info, cnt, ignore_subbeats),
        );

        // Send the ChannelMessage to Flutter and wait for the response
        let response = engine.send_channel_message(message).await;

        // Process the response from Flutter
        match response {
            Ok(ChannelMessageResponse::Success(response_data)) => {
                // Handle the response data from Flutter
                // ...
            }
            Ok(ChannelMessageResponse::Error(error_message)) => {
                // Handle the error message from Flutter
                // ...
            }
            Err(error) => {
                // Handle the error
                // ...
            }
        }

        // Call the build method of MyWidget in Flutter
        let build_message = ChannelMessage::new("build", "");
        let build_response = engine.send_channel_message(build_message).await;

        // Process the response from Flutter
        match build_response {
            Ok(ChannelMessageResponse::Success(response_data)) => {
                // Handle the response data from Flutter
                // ...
            }
            Ok(ChannelMessageResponse::Error(error_message)) => {
                // Handle the error message from Flutter
                // ...
            }
            Err(error) => {
                // Handle the error
                // ...
            }
        }
    }
}

impl FMTickerBase for FMCircleTicker {
    fn tick_callback(&mut self, section_info: FMBarElement, cnt: i32, ignore_subbeats: Option<bool>) {
        // Access the class variables using self
        let cwidth = self.cwidth;
        let cheight = self.cheight;
        // Implement the logic for tick_callback
    }

    fn fix_subbeat(&mut self, tick_value: i32, ignore_subbeats: Option<bool>) {
        // Access the class variables using self
        let cwidth = self.cwidth;
        let cheight = self.cheight;
        // Implement the logic for fix_subbeat
    }
}

impl FMCircleTicker {
    fn new(page: Page, timer: Option<FMSectionTimer>) -> Self {
        let cwidth = page.width();
        let cheight = page.height() * 0.4;
        let base_diameter = cwidth * 0.3;
        let diam = [base_diameter, base_diameter * 0.45, base_diameter * 0.3];
        let circle_cols_bg = [colors::YELLOW_100, colors::BLUE_100, colors::CYAN_100];

        Self {
            timer,
            page,
            state: FMTickPositions::T_none,
            cwidth,
            cheight,
            base_diameter,
            diam,
            circle_cols_bg,
        }
    }
}