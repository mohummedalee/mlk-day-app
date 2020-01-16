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
                <div class='centered' id='img1desc'></div>\
            </div>\
            <div class='col-lg-5 my-3 imgcontainer' id='img2container'>\
                <img class='img-fluid active' id='img2' src='images/" + picks[1] + ".jpeg'>\
                <div class='centered' id='img2desc'></div>\
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
    var url = api_url + `/api?user=${user_id}&obj1=${obj1}&obj2=${obj2}&question=${ques}&answer=${ans}`
    $.get(url, null);
}

function record_response(uid, ques, obj1, obj2, ans) {
    cs_answers[qno.toString()] = [obj1, obj2, ans];    // client side
    // mark the chosen image
    if (ans == obj1) {
        $(`#q${qno}`).find('#img1container').css("background-color","#007bff88")
    } else {
        $(`#q${qno}`).find('#img2container').css("background-color","#007bff88")
    }
    console.log(uid, ques, obj1, obj2, ans);
    // send details to backend
    send_to_backend(uid, ques, obj1, obj2, ans);
    modify_old();   // fade out old images
    add_prompt();   // add new question and scroll to it
}


function highlight_answers() {
    // gives feedback based on cs_answers and stats dictionaries
    var key = "frac_men";
    var correct_ans_count = 0;
    if (ques_type == "race") {
        key = "frac_white";
    }


    for (var i = 1; i < qno; i++) {
        // unpack client-side answers
        var img1 = cs_answers[i][0];
        var img2 = cs_answers[i][1];
        var ans = cs_answers[i][2];

        var correct_ans = img2;
        var correct_ans_str = "img2";
        var incorrect_ans_str = "img1";
        if (stats[img1][key] < stats[img2][key]) {
            correct_ans = img1;
            correct_ans_str = "img1";
            incorrect_ans_str = "img2";
        }


        if (ans == correct_ans) {
            $(`#q${i}`).find(`#${correct_ans_str}container`).css("background-color","#28a74588")
            correct_ans_count += 1;
        } else {
            $(`#q${i}`).find(`#${incorrect_ans_str}container`).css("background-color","#dc354588")
        }

        if (key == "frac_men") {
            $(`#q${i}`).find("#img1desc").text(
                `${((1-stats[img1]["frac_men"])*100).toFixed(0)}% female`
            );
            $(`#q${i}`).find("#img2desc").text(
                `${((1-stats[img2]["frac_men"])*100).toFixed(0)}% female`
            );
        } else {
            $(`#q${i}`).find("#img1desc").text(
                `${((1-stats[img1]["frac_white"])*100).toFixed(0)}% Black`
            );
            $(`#q${i}`).find("#img2desc").text(
                `${((1-stats[img2]["frac_white"])*100).toFixed(0)}% Black`
            );
        }

    }

    return correct_ans_count;
}

function show_results(correct_count) {
    // turn off display: none
    $('.info').fadeIn('slow');

    var results_panel =
    `<div class="card text-white bg-info mb-5 text-center offset-lg-4 col-lg-4">\
        <div class="card-header"><h5>Results</h5></div>\
            <div class="card-body">\
            <h3 class="card-title">You got ${correct_count}/${qno-1} correct.</h3>\
            <p class="card-text">Scroll up to see how your predictions compare to Facebook's classification system used in advertising.</p>\
        </div>\
    </div>`;

    $(`#q${qno}`).hide();
    $(`#q${qno}`).html(results_panel).fadeIn();
}
