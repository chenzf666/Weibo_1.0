let pic = $("#picture");
if (pic !== undefined) {
    (function () {
        pic.after("<input type='hidden' id='imgArray' name='imgArray' value=''/>");
        pic.after("<ul id='ulPic'></ul>", "<p class='hint' style='color:red;overflow:hidden;height:0;'>请放入图片!</p>");

        let oUl = $("#ulPic");
        oUl.on('mouseenter', 'div', function () {
            $(this).find(".delete").show();
        });
        oUl.on('mouseleave', 'div', function () {
            $(this).find(".delete").hide();
        });
        oUl.on('click', 'span', function () {
            let img = $(this).prev();
            let oLi = $(this).parents("li");
            $.post(
                '/upload/cancel?t=' + new Date().getTime(),
                {'src': img.attr('src')},
                function () {
                    let arr = img.attr('src').split('/');
                    let filename = arr[arr.length - 1];
                    let imgArray = $('#imgArray');
                    imgArray.val(imgArray.val().replace(' ' + filename, ''));
                    oLi.remove();
                }
            )
        });
    })();

    //图片上传
    pic.change(function () {
        if (this.files.length === 1) {
            let arr = this.files[0].name.split('.');
            if ('jpg jpe jpeg png gif svg bmp'.indexOf(arr[arr.length - 1]) !== -1) {
                let formDate = new FormData();
                formDate.append('image', this.files[0]);
                $.ajax({
                    url: '/upload?t=' + new Date().getTime(),
                    type: 'post',
                    data: formDate,
                    processData: false,
                    contentType: false,
                    dataType: 'json',
                    success: function (json) {
                        let img = "<li style='padding:5px'>" +
                            "   <div class='imgDiv'>" +
                            "       <img src='" + json['imgURL'] + "' height='150px'/>" +
                            "       <span class='delete glyphicon glyphicon-remove-circle' aria-hidden='true'></span>" +
                            "   </div>" +
                            "</li>";
                        $("#ulPic").append(img);
                        let imgArray = $('#imgArray');
                        imgArray.val(imgArray.val() + ' ' + json['filename']);
                        // 置空文件
                        setTimeout("$('#picture').val('')", 500);
                    }
                });
            } else {
                setTimeout("$('#picture').val('')", 500);
                $('.hint').animate({height: '0px'}, 'slow').animate({height: '30px'}, 'slow');
                setTimeout("$('.hint').animate({height:'0px'}, 'slow')", 2500);
            }
        }
    });
}

(function () {
    // show shadow
    let shadow = $(".shadow");
    shadow.on('mouseenter', '.post,.comment', function () {
        $(this).css('background-color', 'rgba(0, 0, 0, .1)');
    });
    shadow.on('mouseleave', '.post,.comment', function () {
        $(this).css('background-color', 'rgba(0,0,0,0)');
    });
})();
