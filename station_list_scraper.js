// used to grab station names in order
// some editing was necesary to match the format in Station_lat_lng.csv
// edited from source: https://stackoverflow.com/questions/6619805/select-text-in-a-column-of-an-html-table

function SelectColumn(index, tableId) {
    var columnText = '\'';
    var columnSelector = '#' + tableId + ' tbody > tr > td:nth-child(' + (index + 1) + ')';
    var cells = $(columnSelector);

    // clear existing selections
    if (window.getSelection) { // all browsers, except IE before version 9
        window.getSelection().removeAllRanges();
    }


    if (document.createRange) {
        cells.each(function(i, cell) {
            var rangeObj = document.createRange();
            rangeObj.selectNodeContents(cell);
            window.getSelection().addRange(rangeObj);
            columnText = columnText + '\',\'' + rangeObj.toString();
        });


    }

    console.log(columnText + '\'');
}