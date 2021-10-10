$(".modal-open").click( function(){
    targetId=$(this).val();
    //キーボード操作などにより、オーバーレイが多重起動するのを防止する
    $(this).blur() ;	//ボタンからフォーカスを外す
    if($("#modal-overlay")[0]) return false ;		//新しくモーダルウィンドウを起動しない [下とどちらか選択]
    //if($("#modal-overlay")[0]) $("#modal-overlay").remove() ;		//現在のモーダルウィンドウを削除して新しく起動する [上とどちらか選択]
    
    if (targetId == "#set_filter"){
        //オーバーレイ用のHTMLコードを、[body]内の最後に生成する
        $("body").append('<div id="modal-overlay-clear"></div>');
        overlay = "#modal-overlay-clear"
    } else {
        //オーバーレイ用のHTMLコードを、[body]内の最後に生成する
        $("body").append('<div id="modal-overlay"></div>');
        overlay = "#modal-overlay"
    }
    
    
    //[$modal-overlay]をフェードインさせる
    $(overlay).fadeIn("slow");
    
    //コンテンツをセンタリングする
    if (targetId != "#set_filter")centeringModalSyncer(targetId);
    
    //コンテンツをフェードインする
    $( targetId).fadeIn( "slow" );
    
    $(overlay + ",#modal-close").unbind().click(function(){
        //[#modal-overlay]と[#modal-close]をフェードアウトする
        $(targetId+","+overlay).fadeOut("slow",function(){
            //フェードアウト後、[#modal-overlay]をHTML(DOM)上から削除
            $(overlay).remove();
        });
    });
    
});


//センタリングを実行する関数
function centeringModalSyncer(targetId) {

    //画面(ウィンドウ)の幅、高さを取得
    var w = $( window ).width() ;
    var h = $( window ).height() ;

    // コンテンツ(#modal-content)の幅、高さを取得
    var cw = $( targetId ).outerWidth();
    var ch = $( targetId ).outerHeight();

    //センタリングを実行する
    $( targetId ).css( {"left": ((w - cw)/2) + "px","top": ((h - ch)/2) + "px"} ) ;

}