var num = 1;

var createInputs = function () {
  $("#ip_div").append('<form id="form"></form>');
  for (var i = 0; i < num; i++) {
    $("#form").append("<input></input>");
  }
};

$("#btn").click(function () {
  createInputs();
  $("#form")
    .find("input")
    .each(function (i) {
      $(this).attr("id", "num" + i);
      $(this).attr("placeholder", "num" + i);
    });
});
