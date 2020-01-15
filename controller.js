const EXPERIMENTS = ["b_o_f", "b_o_m", "b_y_f", "b_y_m", "w_o_f", "w_o_m", "w_y_f", "w_y_m", "beach",
    "skatepark", "basketball", "baseball", "violin", "nightclub", "mansion", "library",
    "gym", "street-fashion", "old-watch", "new-watch", "old-car", "new-car", "old-men-fashion",
    "new-men-fashion", "old-phone", "new-phone", "police", "firefighter", "soldier", "doctor",
    "construction-worker", "professor", "business-executive", "hipster", "school-teacher",
    "programmer", "protester", "science-lab", "computer", "graduation", "college-student", "panel-discussion", "lecture"]

function pick_random_img(){
    var p1 = EXPERIMENTS[Math.floor(Math.random() * EXPERIMENTS.length)];
    var p2 = p1;
    while (p2 == p1) {
        p2 = EXPERIMENTS[Math.floor(Math.random() * EXPERIMENTS.length)];
    }
    return [p1, p2];
}

function reload_image() {
    var picks = pick_random_img();
    $("#img1").attr("src", "images/" + picks[0] + ".jpeg");
    $("#img2").attr("src", "images/" + picks[1] + ".jpeg");

    document.getElementById("question").innerHTML = question();
}

function add_prompt(){
    qno += 1;
    var picks = pick_random_img();
    // update global variables
    curr_img1 = picks[0];
    curr_img2 = picks[1];
    var div_to_add = "\
    <div class='well text-center prompt' id=q" + qno + ">\
        <div class='row col-lg-12'>\
            <div class='offset-lg-1 col-lg-5 my-3 imgcontainer' id='img1container'>\
                <img class='img-fluid active' id='img1' src='images/" + picks[0] + ".jpeg'>\
                <div class='info img1_info'></div>\
            </div>\
            <div class='col-lg-5 my-3 imgcontainer' id='img2container'>\
                <img class='img-fluid active' id='img2' src='images/" + picks[1] + ".jpeg'>\
                <div class='info img2_info'></div>\
            </div>\
        </div>\
    </div>";

    $("#prompt-holder").append(div_to_add);
    $('html,body').animate({
        scrollTop: $(".active").offset().top
    }, 1000);
}

function modify_old(){
    $(".active").fadeTo('slow', 0.2);
    $(".active").removeClass("active");
}

function send_to_backend(uid, ques, obj1, obj2, ans) {
    // FIXME: fails CORS policy for now, this could be served from 0.0.0.0 too
    var url = `http://0.0.0.0:8003/api?obj1=${obj1}&obj2=${obj2}&question=${ques}&answer=${ans}`
    $.get(url, null);
}

function record_response(uid, ques, obj1, obj2, ans) {
    cs_answers[qno.toString()] = [obj1, obj2, ans];    // client side
    // mark the chosen image
    if (ans == obj1) {
        $(`#q${qno}`).find('#img1').addClass("border border-primary rounded");
        $(`#q${qno}`).find('#img1container').css("background-color","#007bff").css("opacity", .5)
    } else {
        $(`#q${qno}`).find('#img2').addClass("border border-primary rounded");
        $(`#q${qno}`).find('#img2container').css("background-color","#007bff").css("opacity", .5)
    }
    console.log(uid, ques, obj1, obj2, ans);
    // send details to backend
    send_to_backend(uid, ques, obj1, obj2, ans);
    modify_old();   // fade out old images
    add_prompt();   // add new question and scroll to it
}

function show_results() {
    // gives feedback based on cs_answers and stats dictionaries
    for (var i = 1; i < qno; i++) {
        // unpack client-side answers
        var img1 = cs_answers[i][0];
        var img2 = cs_answers[i][1];
        var ans = cs_answers[i][2];

        // show stats for first image
        console.log(`#q${i}`);
        $(`#q${i}`).find('.img1_info').html(
            `<p>Men reached: ${stats[img1]["male"]} (${(stats[img1]["frac_men"]*100).toFixed(2)}%).</p>`
        )
        // ...for second image
        $(`#q${i}`).find('.img2_info').html(
            `<p>Men reached: ${stats[img2]["male"]} (${(stats[img2]["frac_men"]*100).toFixed(2)}%).</p>`
        )

        // tell users if their answers were right -- too tired to write fancy logic
        if (ques_type == "gender") {
            if (stats[img1]["frac_men"] > stats[img2]["frac_men"]) {
                if (ans == img1) {
                    $(`#q${i}`).find('.img1_info').addClass("border border-success rounded");
                }
                else {
                    $(`#q${i}`).find('.img2_info').addClass("border border-danger rounded");
                }
            } else {
                if (ans == img2) {
                    $(`#q${i}`).find('.img2_info').addClass("border border-success rounded");
                }
                else {
                    $(`#q${i}`).find('.img1_info').addClass("border border-danger rounded");
                }
            }
        } else {
            // we were asking about race
        }
    }

    // turn off display: none
    $('.info').fadeIn('slow');

    // show user summary of their answers

}
