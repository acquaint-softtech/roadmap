
function UserEdit() {
    return {
      item_search: "",
      comment_search:"",
      vote_search:"",
      pageNumber: 0,
      delete_popup:false,
      delete_popup_header_text:'',
      delete_popup_url:'',
      sortCol:null,
      size: 5,
      total: "",
      items: items,
      comments: comments,
      votes:votes,
      options:['5','10','25','50','All'],
      activeTab:0,
      get user_items() {
        const start = this.pageNumber * this.size,
        end = start + this.size;
        if (this.item_search === "") {
          this.total = this.items.length;
          return this.items.slice(start, end);
        }
        if (this.activeTab === 0){
            this.total = this.items.filter((item) => {
              return (item.name.toLowerCase().includes(this.item_search.toLowerCase()) || item.project__title.toLowerCase().includes(this.item_search.toLowerCase()) || item.type__name.toLowerCase().includes(this.item_search.toLowerCase()))
            }).length;
            return this.items
              .filter((item) => {
                     return item.name.toLowerCase().includes(this.item_search.toLowerCase()) || item.project__title.toLowerCase().includes(this.item_search.toLowerCase()) || item.type__name.toLowerCase().includes(this.item_search.toLowerCase())
              })
            .slice(start, end);
        }
      },
      get user_comments() {
        const start = this.pageNumber * this.size,
         end = start + this.size;
        if (this.comment_search === "") {
          this.total = this.comments.length;
          return this.comments.slice(start, end);
        }
        if (this.activeTab === 1){
            this.total = this.comments.filter((item) => {
              return (item.task__name.toLowerCase().includes(this.comment_search.toLowerCase()) || item.text.toLowerCase().includes(this.comment_search.toLowerCase()))
            }).length;
            return this.comments
              .filter((item) => {
                     return item.task__name.toLowerCase().includes(this.comment_search.toLowerCase()) || item.text.toLowerCase().includes(this.comment_search.toLowerCase())
              })
            .slice(start, end);
        }
      },
      get user_votes() {
        const start = this.pageNumber * this.size,
        end = start + this.size;
        if (this.vote_search === "") {
          this.total = this.votes.length;
          return this.votes.slice(start, end);
        }
        if (this.activeTab === 2){
            this.total = this.votes.filter((item) => {
              return (item.task__name.toLowerCase().includes(this.vote_search.toLowerCase()) || item.task__project__title.toLowerCase().includes(this.vote_search.toLowerCase()))
            }).length;
            return this.votes
              .filter((item) => {
                     return item.task__name.toLowerCase().includes(this.vote_search.toLowerCase()) || item.task__project__title.toLowerCase().includes(this.vote_search.toLowerCase())
              })
             .slice(start, end);
            }
        },

      changePageSize(index){
          this.size = 10
          this.filteredEmployees
      },

      showingPopup(name,url){
        this.delete_popup_header_text = 'Delete ' + name
        this.delete_popup_url = url
        this.delete_popup = true
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

      //Next Page
      nextPage() {
        this.pageNumber++;
      },

      //Previous Page
      prevPage() {
        this.pageNumber--;
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
