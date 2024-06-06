// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable();
});

$(document).ready(function() {
  $('#dataTable-report').DataTable(
    {
        dom: 'Bfrtip',
        buttons: [
          {
              extend: 'pdf',
              split: ['excel','csv']
          }
        ]
    });
});


// $(document).ready(function() {

//   $('#example34').DataTable({

//     language : {
//       searchBuilder: {
//         button : 'Filter',
//       }
//     },
//     buttons: [
//         'searchBuilder'
//     ],
//     dom: 'Bfrtip',

//   });
//   table.searchBuilder.container().prependTo(table().container());

// });


// $(document).ready(function() {
//   var table = $('#example24').DataTable({
//     searchBuilder: true
//   });
//   table.searchBuilder.container().prependTo(table().container());
// })

// $(document).ready(function() {

//   $.fn.dataTable.moment( 'HH:mm, MMMM D, YY');
//   $.fn.dataTable.moment( 'ddd, MMMM Do, YYYY');

//   $('#example3').DataTable({
//     dom: 'Qlfrtip',

//   });

// });


$(document).ready(function() {
    $('#file-export').DataTable({
        dom: 'Bfrtip',
        buttons: [
          {
              extend: 'pdf',
              split: ['excel','csv']
          }
        ]
        
    } );

} );
    




