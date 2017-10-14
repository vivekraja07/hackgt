/*  This visualization was made possible by modifying code provided by:

Scott Murray, Choropleth example from "Interactive Data Visualization for the Web"
https://github.com/alignedleft/d3-book/blob/master/chapter_12/05_choropleth.html

Malcolm Maclean, tooltips example tutorial
http://www.d3noob.org/2013/01/adding-tooltips-to-d3js-graph.html

Mike Bostock, Pie Chart Legend
http://bl.ocks.org/mbostock/3888852  */


//Width and height of map
var width = 960;
var height = 500;

// D3 Projection
var projection = d3.geo.albersUsa()
           .translate([width/2, height/2])    // translate to center of screen
           .scale([1000]);          // scale things down so see entire US

// Define path generator
var path = d3.geo.path()               // path generator that will convert GeoJSON to SVG paths
         .projection(projection);  // tell path generator to use albersUsa projection


// Define linear scale for output
var color = d3.scale.linear()
        .range(["rgb(213,222,217)","rgb(69,173,168)","#22593b","rgb(217,91,67)"]);

//Create SVG element and append map to the SVG
var svg = d3.select("body")
      .append("svg")
      .attr("id","map")
      .attr("width", width)
      .attr("height", height);

// Append Div for tooltip to SVG
var div = d3.select("body")
        .append("div")
        .attr("class", "tooltip")
        .style("opacity", 0);

// Load in my states data!
d3.csv("stateslived.csv", function(data) {
color.domain([0,1,2,3]); // setting the range of the input data

// Load GeoJSON data and merge with states data
d3.json("us-states.json", function(json) {

// Loop through each state data value in the .csv file
for (var i = 0; i < data.length; i++) {

  // Grab State Name
  var dataState = data[i].state;

  // Grab data value
  var dataValue = data[i].visited;

  // Find the corresponding state inside the GeoJSON
  for (var j = 0; j < json.features.length; j++)  {
    var jsonState = json.features[j].properties.name;

    if (dataState == jsonState) {

    // Copy the data value into the JSON
    json.features[j].properties.visited = dataValue;

    // Stop looking through the JSON
    break;
    }
  }
}

// Bind the data to the SVG and create one path per GeoJSON feature
svg.selectAll("path")
  .data(json.features)
  .enter()
  .append("path")
  .attr("d", path)
  .style("stroke", "#fff")
  .style("stroke-width", "2")
  .style("fill", function(d) {

  // Get data value
  var value = d.properties.visited;

  if (value) {
  //If value exists…
  return color(value);
  } else {
  //If value is undefined…
  return "rgb(213,222,217)";
  }
});


// Map the cities I have lived in!
d3.csv("cities.csv", function(data) {

svg.selectAll("circle")
  .data(data)
  .enter()
  .append("circle")
  .attr("cx", function(d) {
    return projection([d.lon, d.lat])[0];
  })
  .attr("cy", function(d) {
    return projection([d.lon, d.lat])[1];
  })
  .attr("r", function(d) {
    return Math.sqrt(d.transactions) * 5;
  })
    .style("fill", "rgb(217,91,67)")
    .style("opacity", 0.85)

  // Modification of custom tooltip code provided by Malcolm Maclean, "D3 Tips and Tricks"
  // http://www.d3noob.org/2013/01/adding-tooltips-to-d3js-graph.html
  .on("mouseover", function(d) {
      div.transition()
           .duration(200)
           .style("opacity", .9);
      div.text(d.city)
           .style("left", (d3.event.pageX) + "px")
           .style("top", (d3.event.pageY) + "px");
      if (d.city != "New York City") {
        getCity(d.city.split(' ').join(''));
      } else {
        var resp = getCity('NewYork');
        getCity('NewYork');
      }

  })

    // fade out tooltip on mouse out
    .on("mouseout", function(d) {
        div.transition()
           .duration(500)
           .style("opacity", 0);
    });
});
  });

});
