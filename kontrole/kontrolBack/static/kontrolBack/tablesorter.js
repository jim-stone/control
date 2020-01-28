
$(document).ready(function() {
    console.log("LOADED");
    $(".tablesorter").tablesorter({
        theme: 'bootstrap',
        widgets: ['filter', 'columns', 'zebra'],
        
        // widthFixed: true,

        widgetOptions : {
            // using the default zebra striping class name, so it actually isn't included in the theme variable above
            // this is ONLY needed for bootstrap theming if you are using the filter widget, because rows are hidden
            zebra : ["even", "odd"],
      
            // class names added to columns when sorted
            columns: [ "primary", "secondary", "tertiary" ],
      
            // reset filters button
            filter_reset : ".reset",
      
            // extra css class name (string or array) added to the filter element (input or select)
            filter_cssFilter: [
              'form-control',
              'form-control',
              'form-control custom-select', // select needs custom class names :(
              'form-control',
              'form-control',
              'form-control',
              'form-control'
            ]
      
          }
    });
  });