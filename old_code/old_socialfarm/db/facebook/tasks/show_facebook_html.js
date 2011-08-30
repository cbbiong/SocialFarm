function(doc, req) { 
	var Mustache = require( "common/js/mustache" );
	var page_template = this.facebook.html.tasks.show_facebook_html ;  
	var navigation_template = this.facebook.html.navigation ;

    //doc.task = JSON.stringify(doc);

	nav = Object() ;
	nav.bid = String(req['path']).split(',')[0] ;
	nav.tasks_class = 'active' ;

    if (doc._attachments){
        var docs = Array();
        for (a in doc._attachments){
            docs.push({"name":a});
        }
        doc._attachments = docs;
    }

	if (doc.data_items){
        var items = Array();
        for (k in doc.data_items){
            items.push({"key":k, "value": doc.data_items[k]});
        }
        doc.data_items = items;
    }

    doc.bid = nav.bid ;

	doc.navigation = Mustache.to_html( navigation_template, nav ) ;
	doc.default_css = this.common.html.default_css ; 
    doc.default_js = this.common.html.default_js ; 
	doc.facebook_footer = this.facebook.html.facebook_footer ;
	return Mustache.to_html( page_template, doc ) ; 
} 

