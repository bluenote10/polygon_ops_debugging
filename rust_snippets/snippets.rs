// To write GeoJSON with plain serde:
use geojson::{GeoJson, Feature, FeatureCollection, Value, Geometry};

let output_geojson = GeoJson::FeatureCollection(FeatureCollection {
  bbox: None,
  features: output_features,
  foreign_members: None,
});
let f = File::create(filename).expect("Unable to create json file.");
serde_json::to_writer_pretty(f, &output_geojson).expect("Unable to write json file.");



// Alternative implementation of next-pos-loop
let mut pos = i;

let initial = result_events[pos as usize].point;
contour.points.push(initial);

loop {
    println!("pos = {}   {}   {:?} => {:?}",
        pos,
        if result_events[pos as usize].is_left() { "L" } else { "R" },
        result_events[pos as usize].point,
        result_events[pos as usize].get_other_event().unwrap().point,
    );

    mark_as_processed(&mut processed, &result_events, pos, contour_id);

    pos = result_events[pos as usize].get_pos();
    println!("Jump pos: {}", pos);

    mark_as_processed(&mut processed, &result_events, pos, contour_id);

    // This would be an alternative exit point: Check we have reached the
    // starting point, after following the edge, but before calling the
    // search for possible continuation. With this termination condition
    // we should never reach the point where next_pos fails and returns
    // -1.
    if result_events[pos as usize].point == initial {
        break;
    }

    contour.points.push(result_events[pos as usize].point);
    pos = next_pos(pos, &result_events, &processed, i);
    println!("Next pos: {}", pos);

    if pos < 0 /*|| result_events[pos as usize].point == initial*/ {
        break;
    }
}

// Version with debug output
let orig_pos = i; // alias just clarity
let mut pos = i;

let initial = result_events[pos as usize].point;
contour.points.push(initial);

loop {
    println!("pos = {}   {}   {:?} => {:?}",
        pos,
        if result_events[pos as usize].is_left() { "L" } else { "R" },
        result_events[pos as usize].point,
        result_events[pos as usize].get_other_event().unwrap().point,
    );

    mark_as_processed(&mut processed, &result_events, pos, contour_id);

    pos = result_events[pos as usize].get_pos();
    println!("Jump pos: {}", pos);

    mark_as_processed(&mut processed, &result_events, pos, contour_id);

    contour.points.push(result_events[pos as usize].point);
    pos = next_pos(pos, &result_events, &processed, orig_pos);
    println!("Next pos: {}", pos);

    if pos == i {
        break;
    }
}

debug_assert_eq!(contour.points.first(), contour.points.last());
//debug_assert_ne!(pos, -1);






// Contour tracking:
let contour_id = result.len() as i32;
println!("\n *** Adding contour id {}", contour_id);
//depth.insert(contour_id, 0);
//hole_of.insert(contour_id, -1);

if let Some(prev_in_result) = result_events[i as usize].get_prev_in_result() {
    let lower_contour_id = prev_in_result.get_output_contour_id();
    println!("Inferring information from lower_contour_id = {} with result transition = {:?}", lower_contour_id, prev_in_result.get_result_transition());
    println!("{:?}", prev_in_result.point);
    println!("{:?}", prev_in_result.get_other_event().unwrap().point);
    if prev_in_result.get_result_transition() == ResultTransition::OutIn {
        // We are inside, let's check if the thing below us is an exterior contour or just
        // another hole.
        let lower_contour = &result[lower_contour_id as usize];
        if result[lower_contour_id as usize].is_exterior {
            result[lower_contour_id as usize].hole_ids.push(contour_id);
            //hole_of.insert(contour_id, lower_contour_id);
            //depth.insert(contour_id, depth[&lower_contour_id] + 1);
            contour.hole_of = Some(lower_contour_id);
            contour.depth = result[lower_contour_id as usize].depth + 1;
            contour.is_exterior = false;
            //println!("Marking contour as hole of {} with depth {}", lower_contour_id, depth[&contour_id]);
        } else {
            if let Some(parent_contour_id) = lower_contour.hole_of {
                result[parent_contour_id as usize].hole_ids.push(contour_id);
                //hole_of.insert(contour_id, parent_contour_id);
                //depth.insert(contour_id, depth[&lower_contour_id]);
                contour.hole_of = Some(parent_contour_id);
                contour.depth = result[lower_contour_id as usize].depth;
                contour.is_exterior = false;
                //println!("Transitively marking contour as hole of {} via {} with depth {}", parent_contour_id, lower_contour_id, depth[&contour_id]);
            }
        }
    } else {
        contour.is_exterior = true;
        println!("Keeping contour as external");
    }
}


//-----------------------------------------------------------------------------
// connect_edges debugging
//-----------------------------------------------------------------------------

// at the end of `order_events`
for r in &result_events {
    println!("{:?}", r);
    debug_assert!(r.get_other_event().is_some());
}

for (i, r) in result_events.iter().enumerate() {
    println!("pos {:3} linked to {:3}    {}    {:?} => {:?}",
        i,
        r.get_other_pos(),
        if r.is_left() { "L" } else { "R" },
        r.point,
        r.get_other_event().map(|o| o.point).unwrap(),
    );
}

// csv generator
use std::fs::File;
use std::io::Write;
fn debug_print_results<F>(events: &[Rc<SweepEvent<F>>])
where
    F: Float,
{
    let mut writer = File::create("debug.csv").unwrap();
    writeln!(&mut writer,
        "index;x;y;other_x;other_y;lr;result_transition;in_out;other_in_out;is_subject;is_exterior_ring;prev_in_result"
    ).expect("Failed to write to file");
    for (i, evt) in events.iter().enumerate() {
        writeln!(&mut writer, "{i};{x:?};{y:?};{other_x:?};{other_y:?};{lr};{transition:?};{in_out};{other_in_out};{subject};{exterior_ring};{prev_in_result:?}",
            i=i,
            x=evt.point.x,
            y=evt.point.y,
            other_x=evt.get_other_event().unwrap().point.x,
            other_y=evt.get_other_event().unwrap().point.y,
            lr=if evt.is_left() { "L" } else { "R" },
            transition=evt.get_result_transition(),
            in_out=evt.is_in_out(),
            other_in_out=evt.is_other_in_out(),
            subject=evt.is_subject,
            exterior_ring=evt.is_exterior_ring,
            prev_in_result=evt.get_prev_in_result().map(|o| format!("{:?}", o.point)),
        ).expect("Failed to write to file");
    }
}

// to be called in second line of connect edges
debug_print_results(&result_events);