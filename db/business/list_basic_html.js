function (head, req) {   

    var Mustache = require( "common/js/mustache" );
    var page_template = this.common.html.list_basic_html ; 
    var row_template = this.common.html.list_basic_html_row ; 
    var default_css = this.common.html.default_css ; 
	var facebook_footer = this.facebook.html.facebook_footer ; 
	var navigation_template = this.facebook.html.navigation ;

	nav = Object() ;

	navigation = Mustache.to_html( navigation_template, nav )

    // set the content header through the call back 
    start({"headers": {"Content-Type": "text/html"}});

    html_rows = String() ; 
    while( (row = getRow()) ) { 
        html_rows += Mustache.to_html( row_template, row.value );
        //log( " html : " + html_rows ) ; 
    }

    doc = Object() ; 
    doc.default_css = default_css
	doc.navigation = navigation
	doc.facebook_footer = facebook_footer
    doc.numrows = head.total_rows ;
    doc.offset = head.offset ; 
    doc.html_rows = html_rows ; 
    send( Mustache.to_html( page_template, doc ) ) ;
} 
