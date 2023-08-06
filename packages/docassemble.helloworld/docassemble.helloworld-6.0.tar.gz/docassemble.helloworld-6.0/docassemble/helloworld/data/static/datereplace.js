$(document).on('daPageLoad', function(){
  $('input[type="date"]').each(function(){
    var dateElement = this;
    $(dateElement).hide();
    $(dateElement).attr('type', 'hidden');
    var yearElement = $('<select class="form-control">');
    var monthElement = $('<select class="form-control">');
    var today = new Date();
    var dateEntered;
    if ($(dateElement).val()){
      var utcDate = new Date($(dateElement).val());
      dateEntered = new Date(utcDate.getUTCFullYear(), utcDate.getUTCMonth(), utcDate.getUTCDate());
    }
    else{
      dateEntered = today;
    }
    for(var year=today.getFullYear(); year > today.getFullYear() - 50; year--){
      var opt = $("<option>");
      opt.val(year);
      opt.text(year);
      if (year == dateEntered.getFullYear()){
        opt.attr('selected', 'selected');
      }
      yearElement.append(opt);
    }
    for(var month=0; month < 12; month++){
      var opt = $("<option>");
      if (month < 9){
        opt.val('0' + (month + 1));
      }
      else{
        opt.val(month + 1);
      }
      var dt = new Date(1970, month, 1);
      opt.text(dt.toLocaleString('default', { month: 'long' }));
      if (month == dateEntered.getMonth()){
        opt.attr('selected', 'selected');
      }
      monthElement.append(opt);
    }
    function updateDate(){
      $(dateElement).val($(yearElement).val() + '-' + $(monthElement).val() + '-01');
    }
    $(dateElement).after(yearElement);
    $(yearElement).after(monthElement);
    yearElement.on('change', updateDate);
    monthElement.on('change', updateDate);
    updateDate();
  });
});