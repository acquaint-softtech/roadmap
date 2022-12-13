function addTask() {
    return {
        boards: [],
        light : true,
        init(){
            this.light = localStorage.getItem("light") == 'true'
        },
        GetBoards($event) {
            let project_id = $event.target.value
            fetch('/admin/get_project_wise_board/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrf_token },
                body: JSON.stringify({ 'project_id': $event.target.value })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.message == 'success') {
                        let boards = JSON.parse(data.boards)
                        this.boards = boards
                    }
                })
        }
    }
}