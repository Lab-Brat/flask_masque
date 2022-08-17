$(document).ready(function(){
  var max_input_fields = 10;
  var add_input = $('.add-input');
  var input_wrapper = $('.input-wrapper');
  var new_input = '\
  <div>\
  <input type="text" name="field[]" value=""/>\
  <a href="javascript:void(0);" class="remove-input" title="Remove input">\
  <button type="button">Delete</button>\
  </a>\
  </div>';

  var add_input_count = 1; 
  
  $(add_input).click(function(){
      if(add_input_count < max_input_fields){
          add_input_count++; 
          $(input_wrapper).append(new_input); 
      }
  });
  
  $(input_wrapper).on('click', '.remove-input', function(e){
      e.preventDefault();
      $(this).parent('div').remove();
      add_input_count--;
  });
});