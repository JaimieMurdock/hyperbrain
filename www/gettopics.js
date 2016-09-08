var combineWords = function(words) {
   return d3.keys(words).sort(function(a,b) {
              if (words[a] > words[b])
                return -1;
              else if (words[a] < words[b])
                return 1;
              else
                return 0;
            }).join(", ") + ", ..."; 
}

var ks = [20, 40, 60, 80];
var k_urls = ks.map(function(k) { return 'topics/' + k + "/topics.json" });
var topics = Promise.all(k_urls.map($.getJSON)).then(function (data) {
    var t = {}; 
    data.forEach(function(d,i) {
      t[ks[i]] = $.each(d, function(key, val) { d[key] = combineWords(val.words) });
  });
    return t;
});

function gettopics(words) {
  $.getJSON('parents.json', function(parents) { 
    var query = words.map(word => parents[word].map(word => 'abi:' + word).join('|'))
      .join('|');
    //var query = words.join('|');
    $('#wordsDl').html('')
    $.getJSON('topics/topics.json?q=' + query, function(data) {
        Promise.resolve(topics).then(function(val) {  
          for (var i = 0; i < 12; i++) {
            var k = data[i]['k'];
            var t = data[i]['t'];
  
          /*$('#wordsDl').append('<dt><a href="' + k + '/?topic=' + t + '">' +
            'Topic ' + t + 
            ' <small>(k = ' + k + ')</small></a></dt>');
          $('#wordsDl').append('<dd>' + 
            val[k][t] + '</dd>'); }*/
          $('#wordsDl').append('<div class="col-xs-4"><h4><a href="' + k + '/?topic=' + t + '">' +
            'Topic ' + t +
            ' <small>(k = ' + k + ')</small></a></h4><p>' +
            val[k][t] + '</p></div>');
          }
          $('#wordsDl').append('<div class="clear">&nbsp;</div>');
        });
    });
    //$('#wordsDl').append('<iframe class="col-xs-12" style="height:500px;" src="http://inphodata.cogs.indiana.edu:8010/topics?q='+query+'"></iframe>')
  });
}
