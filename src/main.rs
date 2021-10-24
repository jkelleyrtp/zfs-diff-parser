use fxhash::{FxHashMap, FxHashSet};
use std::io::Read;

const NAMES: &[&str] = &[
    "logicalused",
    "compressratio",
    "compression",
    "used",
    "recordsize",
];

fn main() {
    let names = NAMES.iter().copied().collect::<FxHashSet<_>>();

    let d1 = read_file_to_string("data/NEW_LOCAL.txt");
    let d2 = read_file_to_string("data/NEW_REMOTE.txt");

    let local = collect_volume_data(&d1, &names);
    let remote = collect_volume_data(&d2, &names);

    for (local_vol, local_props) in local {
        if let Some(remote_props) = remote.get(local_vol) {
            for (prop, local_value) in local_props {
                if let Some(&remote_value) = remote_props.get(prop) {
                    if remote_value != local_value {
                        println!(
                            "vol: {} - {}: {} | {}",
                            local_vol, prop, local_value, remote_value
                        );
                    }
                }
            }
        }
    }
}

fn read_file_to_string(path: &str) -> String {
    let mut file = std::fs::File::open(path).unwrap();
    let mut contents = String::new();
    file.read_to_string(&mut contents)
        .expect("something went wrong reading the file");
    contents
}

fn collect_volume_data<'a>(
    data: &'a str,
    names: &FxHashSet<&str>,
) -> FxHashMap<&'a str, FxHashMap<&'a str, &'a str>> {
    let mut volumes = FxHashMap::default();
    for line in data.lines() {
        let mut parts = line.split_whitespace();
        let (volume, prop, value) = (
            parts.next().unwrap(),
            parts.next().unwrap(),
            parts.next().unwrap(),
        );

        if names.contains(prop) {
            volumes
                .entry(volume)
                .or_insert_with(FxHashMap::default)
                .insert(prop, value);
        }
    }
    volumes
}
