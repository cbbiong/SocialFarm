function (head, req) {   

    var Mustache = require( "common/js/mustache" );
    var page_template = this.facebook.html.canvas ; 
	var navigation_template = this.facebook.html.navigation ;
	var row_template = this.common.html.list_basic_html_row ; 
    var default_css = this.common.html.default_css ;
    var osn_async = this.common.html.osn_async ;

	nav = Object() ;

	navigation = Mustache.to_html( navigation_template, nav )

    // set the content header through the call back 
    start({"headers": {"Content-Type": "text/html"}});

    html_rows = String() ; 
    while( (row = getRow()) ) { 
        html_rows += Mustache.to_html( row_template, row.value ); 
    }

    doc = Object() ; 
    doc.navigation = navigation ;
    doc.default_css = default_css ;
    doc.numrows = head.total_rows ;
    doc.offset = head.offset ; 
    doc.html_rows = html_rows ; 
    doc.osn_async = osn_async ;
    send( Mustache.to_html( page_template, doc ) ) ;
} 


