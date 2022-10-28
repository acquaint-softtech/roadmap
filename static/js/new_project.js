function NewProject(){
    return {
      AddBoard(){
        const node = document.getElementById("id_projects").lastElementChild;
        const clone = node.cloneNode(true);
        document.getElementById("id_projects").appendChild(clone);
        document.getElementById("id_category_project-TOTAL_FORMS").value = parseInt(document.getElementById("id_category_project-TOTAL_FORMS").value) + 1
        return true
      },
      RemoveBoard(event,index){
        if (parseInt(document.getElementById("id_category_project-TOTAL_FORMS").value) > 1){
          document.getElementById("id_category_project-TOTAL_FORMS").value = parseInt(document.getElementById("id_category_project-TOTAL_FORMS").value) - 1
          event.currentTarget.offsetParent.remove()
        }
      }
    }
  }