
function Myitems() {
    return {
      item_search: "",
      comment_search:"",
      vote_search:"",
      metions_search:"",
      selectedOption:5,
      pageNumber: 0,
      sortCol:null,
      size: 5,
      total: "",
      total_of_items:"",
      total_of_comments:"",
      total_of_votes:"",
      items: items,
      comments: comments,
      votes:votes,
      options:['5','15','25'],
      activeTab:0,
      get user_items() {
        const start = this.pageNumber * this.size,
        end = start + this.size;
        if (this.item_search === "") {
          this.total_of_items = this.items.length;
          return this.items.slice(start, end);
        }
        this.total_of_items = this.items.filter((item) => {
          return (item.name.toLowerCase().includes(this.item_search.toLowerCase()) ||  item.type__name.toLowerCase().includes(this.item_search.toLowerCase()))
        }).length;
        return this.items
          .filter((item) => {
                 return item.name.toLowerCase().includes(this.item_search.toLowerCase()) || item.type__name.toLowerCase().includes(this.item_search.toLowerCase())
          })
        .slice(start, end);
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
        if (this.vote_search === "") {
          this.total_of_votes = this.votes.length;
          return this.votes.slice(start, end);
        }
        this.total_of_votes = this.votes.filter((item) => {
          return (item.task__name.toLowerCase().includes(this.vote_search.toLowerCase()) || item.task__project__title.toLowerCase().includes(this.vote_search.toLowerCase()))
        }).length;
        return this.votes
          .filter((item) => {
                 return item.task__name.toLowerCase().includes(this.vote_search.toLowerCase()) || item.task__project__title.toLowerCase().includes(this.vote_search.toLowerCase())
          })
         .slice(start, end);
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

      ItemPages(){
        return Array.from({
          length: Math.ceil(this.total_of_items / this.size),
        });
      },

      CommentPages(){
        return Array.from({
          length: Math.ceil(this.total_of_comments / this.size),
        });
      },

      VotePages(){
        return Array.from({
          length: Math.ceil(this.total_of_votes / this.size),
        });
      },

      //Next Page
      ItemnextPage() {
        this.pageNumber++;
      },

      //Previous Page
      ItemprevPage() {
        this.pageNumber--;
      },

      //Total number of pages
      ItempageCount() {
        return Math.ceil(this.total_of_items / this.size);
      },
      //Return the start range of the paginated results
      ItemstartResults() {
        return this.pageNumber * this.size + 1;
      },

      //Return the end range of the paginated results
      ItemendResults() {
        let resultsOnPage = (this.pageNumber + 1) * this.size;
        if (resultsOnPage <= this.total_of_items) {
          return resultsOnPage;
        }
        return this.total_of_items;
      },

      //Link to navigate to page
      ItemviewPage(index) {
        this.pageNumber = index;
      },

      ////////////// Comment sections /////////////////////

      CommentnextPage() {
        this.pageNumber++;
      },

      //Previous Page
      CommentprevPage() {
        this.pageNumber--;
      },

      //Total number of pages
      CommentpageCount() {
        return Math.ceil(this.total_of_comments / this.size);
      },
      //Return the start range of the paginated results
      CommentstartResults() {
        return this.pageNumber * this.size + 1;
      },

      //Return the end range of the paginated results
      CommentendResults() {
        let resultsOnPage = (this.pageNumber + 1) * this.size;
        if (resultsOnPage <= this.total_of_comments) {
          return resultsOnPage;
        }
        return this.total_of_comments;
      },

      //Link to navigate to page
      CommentviewPage(index) {
        this.pageNumber = index;
      },

      ////////////// Vote sections /////////////////////

      VotenextPage() {
        this.pageNumber++;
      },

      //Previous Page
      VoteprevPage() {
        this.pageNumber--;
      },

      //Total number of pages
      VotepageCount() {
        return Math.ceil(this.total_of_votes / this.size);
      },
      //Return the start range of the paginated results
      VotestartResults() {
        return this.pageNumber * this.size + 1;
      },

      //Return the end range of the paginated results
      VoteendResults() {
        let resultsOnPage = (this.pageNumber + 1) * this.size;
        if (resultsOnPage <= this.total_of_votes) {
          return resultsOnPage;
        }
        return this.total_of_votes;
      },

      //Link to navigate to page
      VoteviewPage(index) {
        this.pageNumber = index;
      },
    };
}
