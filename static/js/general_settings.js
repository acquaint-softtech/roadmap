 function GeneralSettings(){
      return{
        activeTab : 0,
        og_popup : false,
        boards : boards,
        show_changelog : false,
        init() {
          document.getElementById('id_enable_change_log').checked == true  ? this.show_changelog = true : this.show_changelog = false

        },
        Changelog(event){
          var checked_value = document.getElementById('id_enable_change_log').checked
          this.show_changelog = checked_value
          document.getElementById('id_show_author_log').checked = checked_value
          document.getElementById('id_show_related_item_log').checked = checked_value
        },
        RemoveTag(name){
          data = JSON.parse(JSON.stringify(this.boards))
          if (data.length > 1){
            var index = data.indexOf(name);
            if (index !== -1) {
              data.splice(index, 1);
            }
            this.boards = data
          }
        },
        Addnotification(event){
          const node = document.getElementById("notify_users").lastElementChild;
          const clone = node.cloneNode(true);
          clone.getElementsByClassName('id_notify_username')[0].value = ''
          clone.getElementsByClassName('id_notify_user_email')[0].value = ''
          document.getElementById("notify_users").appendChild(clone);
          return true
        },
         RemoveNotification(event,index){
            event.currentTarget.offsetParent.remove()
        },
        SaveData(){
          var elements = document.getElementById("notify_users").getElementsByClassName('user-data');
          var data = []
          for (let i = 0; i < elements.length; i++) {
            if (elements[i].getElementsByClassName('id_notify_username')[0].value && elements[i].getElementsByClassName('id_notify_user_email')[0].value){
              data.push({"name":elements[i].getElementsByClassName('id_notify_username')[0].value,'email':elements[i].getElementsByClassName('id_notify_user_email')[0].value})
            }
          }
          document.getElementById('id_send_notification_data').value = JSON.stringify(data)
        },
        addTag(event){
             if (event.currentTarget.value.trim().length > 0 ){
               data = JSON.parse(JSON.stringify(this.boards))
               data.push(event.currentTarget.value.trim())
               event.currentTarget.value = ''
               this.boards = data
             }
        }
      }
  }