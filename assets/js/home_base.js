function Base(){
    return {
      showModal: false,
      csrf_token:csrf_token,
      task_title : '',
      task_description : '',
      title_error : false,
      description_error : false,
      init(){
          this.title_error = false
          this.description_error = false
      },
      SubmitItems(){
          this.task_description = '45454'
          if (this.task_title == '' || this.task_description == ''){
              this.task_title == '' ? this.title_error = true : this.title_error = false
              this.description_error == '' ? this.description_error = true : this.description_error = false
              return false
          }
          fetch('/save_task/', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json','X-CSRFToken':csrf_token },
              body: JSON.stringify({'task_title': this.task_title,'task_description':this.task_description})
          })
          .then(response => response.json())
          .then(data => {
              if (data.message == 'success'){
                  window.location.reload()
              }
          })
      }
    }
}