const stepUrl = "drive_train/step"
const speed = 1
var response = "response"

function responseHandler(rp) {
    response = rp
}

function move(translate, rotate) {
    console.log(`translate=${translate}, rotate=${rotate}`)
    $.getJSON(stepUrl, {"translate": translate, "rotate": rotate}, responseHandler)
}

$(document).ready(function () {
        $("#forward").click(
            function () {
                move(speed, 0)
            }
        );
        $("#left").click(
            function () {
                move(0, speed)
            }
        );
        $("#right").click(
            function () {
                move(0, -speed)
            }
        );
        $("#reverse").click(
            function () {
                move(-speed, 0)
            }
        );
    }
)
