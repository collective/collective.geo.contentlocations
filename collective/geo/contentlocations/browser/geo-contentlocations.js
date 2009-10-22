

jq(document).ready(function() {
  var map = cgmap.config.geoshapemap.map;
  var editlayer = new OpenLayers.Layer.Vector("Edit");
  map.addLayer(editlayer);

  function onEditBeforeFeaturesAdded(evt)
  {
    // TODO: maybe check editingpanel.multi (custom attribute) allowing
    // multiple shapes at once. evt object should hold a reference to control
    // to check this attribute (or I need to add this attribute to the
    // editinglayer?
    evt.object.destroyFeatures();
  }

  editlayer.events.register("beforefeaturesadded", editlayer,
                            onEditBeforeFeaturesAdded);

  var editingpanel = new OpenLayers.Control.EditingToolbar(editlayer, {});
  editingpanel.addControls([ new OpenLayers.Control.ModifyFeature(editlayer, {}) ]);

  map.addControl(editingpanel);
  editingpanel.activate();

  function olupdateWidget(evt)
  {
    var out_options = {
      internalProjection: evt.object.map.projection,
      externalProjection: evt.object.map.displayProjection };
    var format = new OpenLayers.Format.WKT(out_options);
    document.getElementById(cgmap.wkt_widget_id).value = format.write(evt.feature);
    format.destroy();
  }

  editlayer.events.register("featureadded", editlayer, olupdateWidget);
  editlayer.events.register("featuremodified", editlayer, olupdateWidget);

  var geomwkt = document.getElementById(cgmap.wkt_widget_id).value;
  var in_options = {
    internalProjection: map.projection,
    externalProjection: map.displayProjection };
  var format = new OpenLayers.Format.WKT(in_options);
  var feat = format.read(geomwkt);
  if (feat)
  {
    editlayer.addFeatures([feat]);
  }

});
