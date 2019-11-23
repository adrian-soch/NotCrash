const Leap = require('leapjs');
 
// Setup Leap loop with frame callback function
var controllerOptions = {};

Leap.loop(controllerOptions, function(frame) {

// Display Pointable (finger) object data
var pointableString = "";
if (frame.pointables.length > 0) {
for (var i = 0; i < frame.pointables.length; i++) {
    var pointable = frame.pointables[i];

    pointableString += "Pointable ID: " + pointable.id + "<br />";
    pointableString += "Belongs to hand with ID: " + pointable.handId + "<br />";
    pointableString += "Length: " + pointable.length.toFixed(1) + " mm<br />";
    pointableString += "Width: "  + pointable.width.toFixed(1) + " mm<br />";
    pointableString += "Direction: " + vectorToString(pointable.direction, 2) + "<br />";
    pointableString += "Tip position: " + vectorToString(pointable.tipPosition) + " mm<br />";
    pointableString += "Tip velocity: " + vectorToString(pointable.tipVelocity) + " mm/s<br />";
}
}

// Display Hand object data
var handString = "";
if (frame.hands.length > 0) {
for (var i = 0; i < frame.hands.length; i++) {
    var hand = frame.hands[i];

    handString += "Hand ID: " + hand.id + "<br />";
    handString += "Direction: " + vectorToString(hand.direction, 2) + "<br />";
    handString += "Palm normal: " + vectorToString(hand.palmNormal, 2) + "<br />";
    handString += "Palm position: " + vectorToString(hand.palmPosition) + " mm<br />";
    handString += "Palm velocity: " + vectorToString(hand.palmVelocity) + " mm/s<br />";
    handString += "Sphere center: " + vectorToString(hand.sphereCenter) + " mm<br />";
    handString += "Sphere radius: " + hand.sphereRadius.toFixed(1) + " mm<br />";
}
}

//Display Frame
var frameString = "Frame ID: " + frame.id  + "<br />"
            + "Timestamp: " + frame.timestamp + " &micro;s<br />"
            + "Hands: " + frame.hands.length + "<br />"
            + "Fingers: " + frame.fingers.length + "<br />";

})