$(document).ready(function(){
	var id = 0;
	$('#formBoard').validate({
		rules: {
			title: "required"
		},
		messages: {
			title: 'Please enter a Board Name',
		}
	})

	
	$('#formLink').validate({
		rules: {
			link: {
				required: true,
			}
		},
		messages: {
			link: {
				required: 'Url field is required',
			}
		},
		submitHandler: function(form){
			id = id+1;
			var temp = id;
		 	$('#addLink').modal('hide');
		 	var link = $('#formLink #id_link').val();
		 	var title = $('#formLink #id_title').val();
		 	var tags = [];
		 	tags = $('#formLink #id_tags').val();
		 	var domain;
		 	if (link.indexOf("://") > -1) {
		 	    domain = link.split('/')[2];
		 	    if (domain.startsWith('www')){
		 	    	domain = domain.substring(4);
		 	    }
		 	}
		 	else {
		 	    domain = link.split('/')[0];
		 	}
		 	domain = domain.split(':')[0];
		 	var prefix = 'http';
			if (link.substr(0, prefix.length) !== prefix)
			{
			    link = 'http://' + link;
			}
	        var formData = {
	            'title': title,
	            'link': link,
	            'tags': tags,
	        };
	        $.ajax({
	            type: 'POST',
	            url: '/'+slug+'/add',
	            data: formData,
	            beforeSend: function(){
	            	if (title != null) {
	            		title = domain;
	            	}
					var task = '<div id="img-'+temp+'" class="col-md-3 col-sm-6 col-xs-12">'+'<a href="'+link+'" target="_blank">'+
						'<div class="card"><div class="img-container"><img src="'+wait+'"></div>'+'<div class="details"><div class="link-title">'+title+'</div></div><div class="hosts">'+
						'<span><object data="http://'+domain+'/favicon.ico" class="favicon-object" type="image/png"><img src="'+favicon+'"></object></span><span class="host-name">'+
						domain+'</span><span class="pull-right tag"> <i class="fa fa-tag mar-r-5" aria-hidden="true"></i> </span>'+
						'</div><div class="clearfix"></div></div></a></div>'
					$('.card-lists').prepend(task);
	            },
	            success: function (data) {
	                $('#formLink').find('input[type=text]').val('');
	                $('#formLink').trigger('reset');
					$('.selectmultiple').select2('data', null);
	                $('.card-lists #img-'+temp+' .img-container img').replaceWith('<i class="fa fa-trash fa-2x pull-right" aria-hidden="true"><input type="hidden" value="'+data.id+'"></i><img src="/media/images/'+data.image+'">')
	                $('.card-lists #img-'+temp+' .link-title').replaceWith('<div class="link-title">'+data.title+'</div>')
	                if(data.tags.length > 0){
	                	var tag_list = '';
	                	var x = 0;
	    				for(i=0;i<data.tags.length;i++){
			                $('.section-tags .tags li').each(function(){
								if( data.tags[i].trim() === $(this).text().trim()) {
									x = 1;
		            			}
			            	});
			            	if (x != 1){
			            		tag_list += '<li><a href="/'+slug+'/'+data.tags[i]+'">'+data.tags[i]+'</a> </li>'
			            	}
			            	x = 0;
	            		}
	            		$('.section-tags .tags').append(tag_list);
            		}
	            },
	        })
		 }
	})

	var delay = (function(){
	  var timer = 0;
	  return function(callback, ms){
	    clearTimeout (timer);
	    timer = setTimeout(callback, ms);
	  };
	})();

	$('#searchForm').submit(function(e){
		e.preventDefault();
	})

	$('#searchForm .input-search').bind('keyup', function (e) {
		if(e.keyCode == 13){
        	e.preventDefault();
    	}
		delay(function(){
			var newContent = $(this.target).val()
			searchLink(newContent)
	    }, 1000 );
    })

    function searchLink(value){
		var query = $('#searchForm .input-search').val();
		var formData = {
			'q': query,
		}
		if (query){
			$.ajax({
				type: 'GET',
				url: '/'+slug+'/search',
				data: formData,
				success: function(data) {
					$('#search-lists').empty();
					if(data.length==0){
						console.log('nodata');
						$('#search-lists').prepend('<a href="" target="_blank"><div class="title">'+
							'No Result Matches your search</div><div class="hosts mar-t-5"></div></a>');
					} else {
						$.each(data, function(index){
							console.log(data[index].fields);
							getSearchData(data[index].fields);
						})
					}
				}
			})
		} else {
			$('#search-lists').empty();
		}
	}

	function getSearchData(data) {
		var markup = '<a href="'+data.link+'" target="_blank">';
			markup += '<div class="title">' + data.title + '</div>';
			markup += '<div class="hosts mar-t-5">' + data.domain + '</div>';
			markup += '</a>';

		return $('#search-lists').prepend(markup);
	}

	$('#editBoard .delete').on('click', function(){
		$('#deleteModal .delete-link a').attr('href','/'+slug+'/delete')
		$('#deleteModal').modal('show');
	})

	$('.card-lists ').on('click', '.card .img-container .fa',function(e){
		e.preventDefault();
		var id = $(this).find('input[type=hidden]').val();
		$('#deleteModal .delete-link a').attr('href', "/link/"+id+"/delete");
		$('#deleteModal').modal('show');
	})

	$('#deleteModal').on('hidden.bs.modal', function () {
        $('#deleteModal .delete-link a').attr('href','')
	})
})


