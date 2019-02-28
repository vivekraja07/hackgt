var pie_svg = d3.select("body")
  .append("svg")
  .attr("id","pie")
  .attr("width",800)
  .attr("height",500)
  .append("g")

pie_svg.append("g")
  .attr("class", "slices");
pie_svg.append("g")
  .attr("class", "labels");
pie_svg.append("g")
  .attr("class", "lines");

var width = 700,
    height = 500,
  radius = Math.min(width, height) / 2;

var pie = d3.layout.pie()
  .sort(null)
  .value(function(d) {
    return d.value;
  });

var arc = d3.svg.arc()
  .outerRadius(radius * 0.7)
  .innerRadius(radius * 0.5);

var outerArc = d3.svg.arc()
  .innerRadius(radius * 0.9)
  .outerRadius(radius * 0.8);

pie_svg.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

var key = function(d){ return d.data.label; };

var color_pie = d3.scale.ordinal()
  .domain(["Frozen", "Health", "Grains", "Fruits & Veggies", "Alcohol", "Foreign",
           "Beverages", "Pet Food", "Pasta & Rice", "Toiletries", "Meats", "Condiments",
           "Breakfast", "Canned Foods", "Dairy", "Cleaning Supplies", "Baby Food",
           "Snacks", "Deli", "Misc"])
  .range(["#7DDF64", "#0dc453", "#719977",  "#22593b", "#0dc453", "#d0743c"]);

function randomData () {
  var labels = color_pie.domain();
  return labels.map(function(label){
    return { label: label, value: Math.random() }
  });
}

getTotal();

function change(data) {
  /* ------- PIE SLICES -------*/
  var slice = pie_svg.select(".slices").selectAll("path.slice")
    .data(pie(data), key);

  slice.enter()
    .insert("path")
    .style("fill", function(d) { return color_pie(d.data.label); })
    .attr("class", "slice");

  slice
    .transition().duration(1000)
    .attrTween("d", function(d) {
      this._current = this._current || d;
      var interpolate = d3.interpolate(this._current, d);
      this._current = interpolate(0);
      return function(t) {
        return arc(interpolate(t));
      };
    })

  slice.exit()
    .remove();

  /* ------- TEXT LABELS -------*/

  var text = pie_svg.select(".labels").selectAll("text")
    .data(pie(data), key);

  text.enter()
    .append("text")
    .attr("dy", ".35em")
    .text(function(d) {
      return d.data.label;
    });

  function midAngle(d){
    return d.startAngle + (d.endAngle - d.startAngle)/2;
  }

  text.transition().duration(1000)
    .attrTween("transform", function(d) {
      this._current = this._current || d;
      var interpolate = d3.interpolate(this._current, d);
      this._current = interpolate(0);
      return function(t) {
        var d2 = interpolate(t);
        var pos = outerArc.centroid(d2);
        pos[0] = radius * (midAngle(d2) < Math.PI ? 1 : -1);
        return "translate("+ pos +")";
      };
    })
    .styleTween("text-anchor", function(d){
      this._current = this._current || d;
      var interpolate = d3.interpolate(this._current, d);
      this._current = interpolate(0);
      return function(t) {
        var d2 = interpolate(t);
        return midAngle(d2) < Math.PI ? "start":"end";
      };
    });

  text.exit()
    .remove();

  /* ------- SLICE TO TEXT POLYLINES -------*/

  var polyline = pie_svg.select(".lines").selectAll("polyline")
    .data(pie(data), key);

  polyline.enter()
    .append("polyline");

  polyline.transition().duration(1000)
    .attrTween("points", function(d){
      this._current = this._current || d;
      var interpolate = d3.interpolate(this._current, d);
      this._current = interpolate(0);
      return function(t) {
        var d2 = interpolate(t);
        var pos = outerArc.centroid(d2);
        pos[0] = radius * 0.95 * (midAngle(d2) < Math.PI ? 1 : -1);
        return [arc.centroid(d2), outerArc.centroid(d2), pos];
      };
    });

  polyline.exit()
    .remove();
};
