$(document).ready(function() {

  clearAndGetIssues();
  registerAddButton();

});

var BASE_URL = 'https://8a5aaf13.ngrok.io/IssueTracker/' + document.getElementsByTagName("title")[0].innerText;

function clearAndGetIssues() {
  var accordion = $('#accordion');
  accordion.empty();
  $.ajax({
    url: BASE_URL,
    method: 'GET'
  }).done(function(result){
    console.log(result)
    result.forEach(function(element) {
      var newCard = $('<div>');
      newCard.addClass('card');

      var cardHeader = $('<div>');
      cardHeader.addClass('card-header');
      cardHeader.attr('id', 'heading'+element.id);
      cardHeader.attr('issue-id', element.id);

      var h5Tag = $('<h5>');
      h5Tag.addClass('mb-0');

      var button = $('<button>');
      button.addClass('btn');
      button.addClass('btn-link');
      button.attr('data-toggle', 'collapse');
      button.attr('data-target', '#collapse' + element.id);
      button.attr('aria-expanded', 'false');
      button.attr('aria-controls', 'collapse' + element.id);
      button.text(element.problem);

      h5Tag.append(button);
      cardHeader.append(h5Tag);
      newCard.append(cardHeader);

      var cardDesc = $('<div>');
      cardDesc.attr('id', 'collapse' + element.id);
      cardDesc.addClass('collapse')
      cardDesc.attr('aria-labelledby', 'heading' + element.id);
      cardDesc.attr('data-parent', '#accordion');

      var contentDiv = $('<div>');
      contentDiv.addClass('card-body');
      contentDiv.html('<p> Data: ' + element.date + ' </p>' + '<p> Autor: ' + element.name + ' </p>' + '<p> Problem: ' + element.problem + ' </p>' + '<p> Rozwiązanie: ' + element.solution + ' </p>');

      cardDesc.append(contentDiv);
      newCard.append(cardDesc);
      createDeleteButton(cardHeader);
      createEditButton(contentDiv,element);
      accordion.append(newCard);
    })
  });
}

function createDeleteButton(listItem) {
  var deleteButton = $('<span>');
  deleteButton.text('Usuń');
  deleteButton.addClass('btn');
  deleteButton.addClass('btn-danger');
  deleteButton.addClass('btn-sm');
  deleteButton.addClass('float-right');
  deleteButton.on('click', function() {
	var result = confirm("Czy na pewno chcesz usunąć problem?");
	if (result) {
		$.ajax({
			   url: BASE_URL + "/" + listItem.attr('issue-id'),
			   contentType: "application/json",
			   method: "DELETE"
		   }).done(function () {
			   clearAndGetIssues();
		   });
	   }
  });
  listItem.append(deleteButton);
}

function createEditButton(listItem, element) {
  var editButton = $('<span>');
  editButton.text('Edit');
  editButton.addClass('btn');
  editButton.addClass('btn-danger');
  editButton.addClass('btn-sm');
  editButton.addClass('float-right');
  editButton.on('click', function() {
            editForm = document.getElementById("form_base").cloneNode(deep = true)
            fields = editForm.getElementsByTagName('input');
            fields[0].value = element.name;
            fields[1].value = element.problem;
            fields[2].value = element.solution;
            editForm.addEventListener('submit', function (e) {
                e.preventDefault();
                var newIssue = {
                    name: fields[0].value,
                    problem: fields[1].value,
                    solution: fields[2].value,
                    date: element.date
                };
                console.log(newIssue);
                console.log(element.id);
                $.ajax({
                    url: BASE_URL + "/" + element.id,
                    data: JSON.stringify(newIssue),
                    contentType: "application/json",
                    method: "PUT"
                }).done(function () {
                    clearAndGetIssues();
                    clearInputFields();
                });                
            });
            listItem.append(editForm)
            this.hidden = true
        });
  
  listItem.append(editButton);
}


function registerAddButton() {
  $('#addButton').on('click', function(e) {
    e.preventDefault();
    var newIssue = {
      name: $('#name').val(),
      problem: $('#problem').val(),
      solution: $('#solution').val()
    };
    console.log(newIssue);
    $.ajax({
           url: BASE_URL,
           data: JSON.stringify(newIssue),
           contentType: "application/json",
           method: "POST"
       }).done(function () {
           clearAndGetIssues();
           clearInputFields();
       });
  })
}

function clearInputFields() {
  $('#name').val('');
  $('#problem').val('');
  $('#solution').val('');
}

function fileringFunction() {
    var input, filter, ul, li, a, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    div = document.getElementsByClassName("card-header");
    for (i = 0; i < div.length; i++) {
        a = div[i].getElementsByClassName("btn btn-link")[0];
        console.log(div[i]);
        txtValue = a.textContent || a.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            div[i].style.display = "";
        } else {
            div[i].style.display = "none";
        }
    }
}
