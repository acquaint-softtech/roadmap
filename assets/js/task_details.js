 CKEDITOR.config.mentions = [
        {
            feed: users,
            marker: '@',
            minChars:0,
            itemTemplate : '<li data-id="{id}"><img src="https://www.gravatar.com/avatar/4544c6cd4cd4fd104b407fc176491507?s=150" alt="{name}" width="50" height="50">{name}</li>',
            outputTemplate : '<p style="color:black">{name}</p>'
        },
    ];

    function setCkeditorData (message_id){
       CKEDITOR.instances[message_id].setData(document.getElementById(("id_child_msg_")+message_id).value)
    }

    function task_details() {
        return {
          sub_btn_text: subscribed == "True" ? 'Unsubscribe' : 'Subscribe',
          vote_btn : is_voted == "True" ? 'Voted' : 'Vote here',
          voted :  is_voted == "True" ? true : false,
          vote_count : vote_count,
          sub_btn_showing : is_voted == "True" ? true : false,
          TaskSubscription() {
            this.formData = {'task_id':task_id}
            fetch('/admin/change_task_subscription_status/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json','X-CSRFToken':csrf_token },
                body: JSON.stringify(this.formData)
            })
            .then(response => response.json())
            .then(data => {
                this.sub_btn_text = data.btn_status
            })
          },
          GiveVote(){
            if (logged_user == 'False'){
              window.location.href = '/login'
            }
            this.formData = {'task_id':task_id}
            fetch('/admin/change_task_vote/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json','X-CSRFToken':csrf_token },
                body: JSON.stringify(this.formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.message == 'success'){
                    if (data.created){
                        this.vote_btn = 'Voted'
                        this.voted = true
                        this.sub_btn_showing = true
                        this.sub_btn_text='Unsubscribe'
                        this.vote_count = parseInt(this.vote_count) + 1
                    }
                    else{
                        this.vote_btn = 'Vote here'
                        this.sub_btn_showing = false
                        this.voted = false
                        this.sub_btn_text='Subscribe'
                        this.vote_count = this.vote_count == 0 ? 0 : this.vote_count - 1
                    }
                }
             })
          }
        }
    }