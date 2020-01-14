const EXPERIMENTS = ["b_o_f", "b_o_m", "b_y_f", "b_y_m", "w_o_f", "w_o_m", "w_y_f", "w_y_m", "beach",
    "skatepark", "basketball", "baseball", "violin", "nightclub", "mansion", "library",
    "gym", "street-fashion", "old-watch", "new-watch", "old-car", "new-car", "old-men-fashion",
    "new-men-fashion", "old-phone", "new-phone", "police", "firefighter", "soldier", "doctor",
    "construction-worker", "professor", "business-executive", "hipster", "school-teacher",
    "programmer", "protester", "science-lab", "computer", "graduation", "college-student", "panel-discussion", "lecture"]

function pick_random_img(){
    // FIXME: could also pass this an array and make sure that none of the random samples match elements in the array
    var p1 = EXPERIMENTS[Math.floor(Math.random() * EXPERIMENTS.length)];
    var p2 = p1;
    while (p2 == p1) {
        p2 = EXPERIMENTS[Math.floor(Math.random() * EXPERIMENTS.length)];
    }
    return [p1, p2];
}
