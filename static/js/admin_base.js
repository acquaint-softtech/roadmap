function adminHome() {
    return {
        user_notifications:user_notifications,
        notification_count:0,
        global_search:'',
        global_search_shown:false,
        tasks:tasks,
        open_toggle:false,
        open_notification:false,
        toggle:false,
        light:true,
        init() {
            this.notification_count = this.user_notifications.length
            this.light = localStorage.getItem("light") == 'true'
        },
        get global_items() {
          if (this.global_search.trim().length == 0) {
           this.global_search_shown = false
           return [];
          }
          else{
              this.global_search_shown = true
              return this.tasks
              .filter((item) => {
                     return item.name.toLowerCase().includes(this.global_search.toLowerCase())
              })
          }
        },
        lightmode(){
          this.light = !(this.light)
          this.open_toggle = !(this.open_toggle)
          localStorage.setItem("light",this.light);
        },
        notification(type){
            this.formData = {'type':type}
            fetch('/admin/notification/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json','X-CSRFToken':csrf_token },
                body: JSON.stringify(this.formData)
            })
            .then(response => response.json())
            .then(data => {
                this.notification_count = 0
                this.isOpen = false
                this.user_notifications = []
            })
        }
    }
}