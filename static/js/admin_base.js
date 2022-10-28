function adminHome() {
    return {
        user_notifications:user_notifications,
        notification_count:0,
        open_toggle:false,
        open_notification:false,
        toggle:false,
        light:true,
        init() {
            this.notification_count = this.user_notifications.length
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