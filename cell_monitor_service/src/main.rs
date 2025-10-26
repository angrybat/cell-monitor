use udev::{Enumerator};
use std::io;

const SKYRC_B6AC_V2_PRODUCT: &str = "C8051F3xx Development Board";

fn main() -> io::Result<()> {
    let mut enumerator = Enumerator::new()?;
    enumerator.match_subsystem("usb")?;
    for device in enumerator.scan_devices()? {
        let is_skyrc_b6ac_v2 = match device.attribute_value("product").map_or(None, |f| f.to_str()) {
            Some(n) => n == SKYRC_B6AC_V2_PRODUCT,
            None => false,
        };
        if is_skyrc_b6ac_v2 {
            println!("SkyRC B6AC V2 connected at {:?}", device.syspath());
        }
    }
    return Ok(())
}
