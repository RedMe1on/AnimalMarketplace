var Autocomplete = function (options) {
  this.form_selector = options.form_selector;
  this.url = options.url || "/search/autocomplete/";
  this.delay = parseInt(options.delay || 300);
  this.minimum_length = parseInt(options.minimum_length || 2);
  this.name_search_limit = options.name_search_limit || 5;
  this.form_elem = null;
  this.query_box = null;
};

Autocomplete.prototype.setup = function () {
  var self = this;

  this.form_elem = $(this.form_selector);
  this.query_box = this.form_elem.find("input[name=q]");

  // Watch the input box.
  this.query_box.on("keyup", function () {
    var query = self.query_box.val();

    if (query.length < self.minimum_length) {
      return false;
    }

    self.fetch(query);
  });

  // On selecting a result, populate the search field.
  this.form_elem.on("click", ".ac-result", function (ev) {
    self.query_box.val($(this).text());
    $(".ac-results").remove();
  });
};

Autocomplete.prototype.fetch = function (query) {
  var self = this;

  $.ajax({
    url: this.url,
    data: {
      q: query,
    },
    success: function (data) {
      self.show_results(data);
    },
  });
};

Autocomplete.prototype.show_results = function (data) {
  // Remove any existing results.
  $(".ac-results").remove();

  var results = data.results || [];
  var results_wrapper = $('<div class="ac-results"></div>');
  var category_elem = $(
    '<div class="category-wrapper"><div class="category-name"></div></div>'
  );
  var base_elem = $(
    '<div class="result-wrapper"><a href="#" class="ac-result"><div class="ac-result-text"></div></a></div>'
  );

  if (results.length > 0) {
    for (var name_search in results[0]) {
      // text_name = results[0][name_search][object]["name"];
      if (results[0][name_search].length > 0) {
        var category_element = category_elem.clone();
        category_element.find(".category-name").text(name_search);
        results_wrapper.append(category_element);

        for (var object in results[0][name_search]) {
          console.log()
          console.log(results[0])
          if (Object.keys(results[0]).length != 1) {
            if (object > this.name_search_limit - 1) {
              break;
            }
          }
          
          var elem = base_elem.clone();
          text_name = results[0][name_search][object]["name"];
          if (text_name.length > 80) {
            text_name = text_name.substring(0, 80);
            text_name += "...";
          }
          elem
            .find(".ac-result")
            .attr("href", `${results[0][name_search][object]["url"]}`);
          elem.find(".ac-result-text").text(text_name);
          results_wrapper.append(elem);
        }
      }
    }
  } else {
    var elem = base_elem.clone();
    elem.text("No results found.");
    results_wrapper.append(elem);
  }

  this.query_box.after(results_wrapper);
};
