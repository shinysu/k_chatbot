var Message;

Message = function (arg) {
		this.text = arg.text, this.message_side = arg.message_side, this.time = arg.time;
		this.draw = function (_this) {
				return function () {
						var $message;
						$message = $($('.message_template').clone().html());
						$message.addClass(_this.message_side).find('.text').html(_this.text);
						$message.addClass(_this.message_side).find('.timestamp').html(_this.time);
						$('.messages').append($message);
						return setTimeout(function () {
								return $message.addClass('appeared');
						}, 0);
				};
		}(this);
		return this;
};


function send_message(start = false)
    {
      query = {"text":$("#msg_input").val()};

      if (query["text"] === "")
        return;
      else{
        showUserMessage($("#msg_input").val());
      }
      $("#msg_input").val("");
      $.ajax({
      type: 'POST',
      url:  "/get_reply" ,
      data: query,
      // dataType: 'json',
      success: function(response) {
        showBotMessage(response["text"])
      },
      error: function(jqXHR, textStatus, errorThrown) {
        // alert('error occured');
      }
    });
    }

function showUserMessage(text,init=false){
    $('#messages').append(
        ` <div class="chat-message usermessage">
                ${text}
            </div>`
    );
	if (!init) {
		$('.messages').animate({ scrollTop: $('.messages').prop('scrollHeight') }, 300);
	}
	$('#msg_input').val('');
}

function showBotMessage(text,init=false){
    $('#messages').append(
        `<div class="chat-message botmessage">
                    ${text}
                </div>`
    );
	if (!init) {
		$('.messages').animate({ scrollTop: $('.messages').prop('scrollHeight') }, 300);
	}
	$('#msg_input').val('');
}
