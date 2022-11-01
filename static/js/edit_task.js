
function TaskEdit() {
    return {
      comment_search:"",
      vote_search:"",
      pageNumber: 0,
      sortCol:null,
      delete_popup:false,
      delete_popup_header_text:'',
      delete_popup_url:'',
      og_popup:false,
      size: 5,
      task_histories: task_histories,
      comments: comments,
      votes:votes,
      change_logs:[],
      total_of_histories : '',
      total_of_comments:'',
      total_of_votes:'',
      options:['5','10','25','50','All'],
      activeTab:0,
      total_comments : '',
      project_id: project_id,
      csrf_token:csrf_token,
      boards : [],
      init() {
        this.Boards(this.project_id)
      },
      Boards($event,project_id){
        $event.target ? project_id = $event.target.value : project_id = $event
        if (project_id != 'None'){
            fetch('/admin/get_project_wise_board/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json','X-CSRFToken':this.csrf_token },
            body: JSON.stringify({'project_id': project_id})
            })
            .then(response => response.json())
            .then(data => {
                if (data.message == 'success'){
                    let boards = JSON.parse(data.boards)
                    this.boards = boards
                }
            })
        }
       },
      get task_histories_data() {
        const start = this.pageNumber * this.size,
        end = start + this.size;
        this.total_of_histories = this.task_histories.length;
        return this.task_histories.slice(start, end);
      },

      get logs() {
        return this.change_logs
      },

      get user_comments() {
        const start = this.pageNumber * this.size,
         end = start + this.size;
        if (this.comment_search === "") {
          this.total_of_comments = this.comments.length;
          return this.comments.slice(start, end);
        }
        this.total_of_comments = this.comments.filter((item) => {
          return (item.task__name.toLowerCase().includes(this.comment_search.toLowerCase()) || item.text.toLowerCase().includes(this.comment_search.toLowerCase()))
        }).length;
        return this.comments
          .filter((item) => {
                 return item.task__name.toLowerCase().includes(this.comment_search.toLowerCase()) || item.text.toLowerCase().includes(this.comment_search.toLowerCase())
          })
        .slice(start, end);

      },
      get user_votes() {
        const start = this.pageNumber * this.size,
        end = start + this.size;
         this.total_of_votes = this.votes.length;
         return this.votes.slice(start, end);
        },

      changePageSize(index){
          this.size = 10
          this.filteredEmployees
      },

      sort(col) {
           if (this.activeTab === 0){
                data = this.items
           }
           if (this.activeTab === 1){
                data = this.comments
           }
           if (this.activeTab === 2){
                data = this.votes
           }
          if(this.sortCol === col) this.sortAsc = !this.sortAsc;
          this.sortCol = col;
          data.sort((a, b) => {
            if(a[this.sortCol] < b[this.sortCol]) return this.sortAsc?1:-1;
            if(a[this.sortCol] > b[this.sortCol]) return this.sortAsc?-1:1;
            return 0;
          });
       },

      //Create array of all pages (for loop to display page numbers)
      pages() {
        return Array.from({
          length: Math.ceil(this.total / this.size),
        });
      },

      showingPopup(name,url){
        this.delete_popup_header_text = 'Delete ' + name
        this.delete_popup_url = url
        this.delete_popup = true
      },

      //Next Page
      nextPage() {
        this.pageNumber++;
      },

      //Previous Page
      prevPage() {
        this.pageNumber--;
      },

      HistoryResults() {
        return this.pageNumber * this.size + 1;
      },

      //Return the end range of the paginated results
      HistoryEndResults() {
        let resultsOnPage = (this.pageNumber + 1) * this.size;
        if (resultsOnPage <= this.total_of_histories) {
          return resultsOnPage;
        }
        return this.total_of_histories;
      },


      CommentResults() {
        return this.pageNumber * this.size + 1;
      },

      //Return the end range of the paginated results
      CommentEndResults() {
        let resultsOnPage = (this.pageNumber + 1) * this.size;
        if (resultsOnPage <= this.total_of_comments) {
          return resultsOnPage;
        }
        return this.total_of_comments;
      },

      VoteResults() {
        return this.pageNumber * this.size + 1;
      },

      //Return the end range of the paginated results
      VoteEndResults() {
        let resultsOnPage = (this.pageNumber + 1) * this.size;
        if (resultsOnPage <= this.total_of_votes) {
          return resultsOnPage;
        }
        return this.total_of_votes;
      },



      //Total number of pages
      pageCount() {
        return Math.ceil(this.total / this.size);
      },
      //Return the start range of the paginated results
      startResults() {
        return this.pageNumber * this.size + 1;
      },

      //Return the end range of the paginated results
      endResults() {
        let resultsOnPage = (this.pageNumber + 1) * this.size;
        if (resultsOnPage <= this.total) {
          return resultsOnPage;
        }
        return this.total;
      },

      //Link to navigate to page
      viewPage(index) {
        this.pageNumber = index;
      },
    };
}
