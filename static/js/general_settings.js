 function GeneralSettings(){
      return{
        activeTab : 0,
        og_popup : false,
        boards : boards,
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