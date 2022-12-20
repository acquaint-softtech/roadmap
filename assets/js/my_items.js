
function Myitems() {
    return {
      item_search: "",
      comment_search:"",
      vote_search:"",
      mention_search:"",
      ItempageNumber: 0,
      VotepageNumber: 0,
      MentionpageNumber: 0,
      CommentpageNumber:0,
      sortCol:null,
      options:options,
      item_page_size: Math.min.apply(Math,this.options),
      vote_page_size: Math.min.apply(Math,this.options),
      mention_page_size: Math.min.apply(Math,this.options),
      comment_page_size: Math.min.apply(Math,this.options),
      total: "",
      total_of_items:"",
      total_of_comments:"",
      total_of_votes:"",
      total_of_mentions:"",
      items: items,
      comments: comments,
      votes:votes,
      mentions:mentions,
      activeTab:0,
      get user_items() {
        const start = this.ItempageNumber * this.item_page_size,
        end = start + this.item_page_size;
        if (this.item_search === "") {
          this.total_of_items = this.items.length;
          return this.items.slice(start, end);
        }
        this.total_of_items = this.items.filter((item) => {
          return (item.name.toLowerCase().includes(this.item_search.toLowerCase()))
        }).length;
        return this.items
          .filter((item) => {
                 return item.name.toLowerCase().includes(this.item_search.toLowerCase())
          })
        .slice(start, end);
      },
      get user_comments() {
        const start = this.CommentpageNumber * this.comment_page_size,
         end = start + this.comment_page_size;
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
        const start = this.VotepageNumber * this.vote_page_size,
        end = start + this.vote_page_size;
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

      get user_mentions(){
        const start = this.MentionpageNumber * this.mention_page_size,
        end = start + this.mention_page_size;
         if (this.mention_search === "") {
          this.total_of_mentions = this.mentions.length;
          return this.mentions.slice(start, end);
        }
        this.total_of_mentions = this.mentions.filter((item) => {
          return (item.task__name.toLowerCase().includes(this.mention_search.toLowerCase()))
        }).length;

        return this.mentions
          .filter((item) => {
                 return item.task__name.toLowerCase().includes(this.mention_search.toLowerCase())
          })
        .slice(start, end);
      },

      MentionchangeSize(page_size){
       page_size != 'All' ? this.mention_page_size = parseInt(page_size) : this.mention_page_size = this.mentions.length
       this.user_mentions
      },

      ItemchangeSize(page_size){
       page_size != 'All' ? this.item_page_size = parseInt(page_size) : this.item_page_size = this.items.length
       this.user_items
      },

      VotechangeSize(page_size){
       page_size != 'All' ? this.vote_page_size = parseInt(page_size) : this.vote_page_size = this.comments.length
       this.user_votes
      },

      CommentchangeSize(page_size){
       page_size != 'All' ? this.comment_page_size = parseInt(page_size) : this.comment_page_size = this.votes.length
       this.user_comments
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
          length: Math.ceil(this.total_of_items / this.item_page_size),
        });
      },

      MentionPages(){
        return Array.from({
          length: Math.ceil(this.total_of_mentions / this.mention_page_size),
        });
      },


//      MentionviewPage

      CommentPages(){
        return Array.from({
          length: Math.ceil(this.total_of_comments / this.comment_page_size),
        });
      },

      VotePages(){
        return Array.from({
          length: Math.ceil(this.total_of_votes / this.vote_page_size),
        });
      },

      //Next Page
      ItemnextPage() {
        this.ItempageNumber++;
      },

      //Previous Page
      ItemprevPage() {
        this.ItempageNumber--;
      },

      //Total number of pages
      ItempageCount() {
        return Math.ceil(this.total_of_items / this.item_page_size);
      },
      //Return the start range of the paginated results
      ItemstartResults() {
        return this.ItempageNumber * this.item_page_size + 1;
      },

      //Return the end range of the paginated results
      ItemendResults() {
        let resultsOnPage = (this.ItempageNumber + 1) * this.item_page_size;
        if (resultsOnPage <= this.total_of_items) {
          return resultsOnPage;
        }
        return this.total_of_items;
      },

      //Link to navigate to page
      ItemviewPage(index) {
        this.ItempageNumber = index;
      },

      ////////////// Comment sections /////////////////////

      CommentnextPage() {
        this.CommentpageNumber++;
      },

      //Previous Page
      CommentprevPage() {
        this.CommentpageNumber--;
      },

      //Total number of pages
      CommentpageCount() {
        return Math.ceil(this.total_of_comments / this.comment_page_size);
      },
      //Return the start range of the paginated results
      CommentstartResults() {
        return this.CommentpageNumber * this.comment_page_size + 1;
      },

      //Return the end range of the paginated results
      CommentendResults() {
        let resultsOnPage = (this.CommentpageNumber + 1) * this.comment_page_size;
        if (resultsOnPage <= this.total_of_comments) {
          return resultsOnPage;
        }
        return this.total_of_comments;
      },

      //Link to navigate to page
      CommentviewPage(index) {
        this.CommentpageNumber = index;
      },

      ////////////// Vote sections /////////////////////

      VotenextPage() {
        this.VotepageNumber++;
      },

      //Previous Page
      VoteprevPage() {
        this.VotepageNumber--;
      },

      //Total number of pages
      VotepageCount() {
        return Math.ceil(this.total_of_votes / this.vote_page_size);
      },
      //Return the start range of the paginated results
      VotestartResults() {
        return this.VotepageNumber * this.vote_page_size + 1;
      },

      //Return the end range of the paginated results
      VoteendResults() {
        let resultsOnPage = (this.VotepageNumber + 1) * this.vote_page_size;
        if (resultsOnPage <= this.total_of_votes) {
          return resultsOnPage;
        }
        return this.total_of_votes;
      },

      //Link to navigate to page
      VoteviewPage(index) {
        this.VotepageNumber = index;
      },

      //////////////////// Mention section ////////////
      MentionnextPage() {
        this.MentionpageNumber++;
      },

      //Previous Page
      MentionprevPage() {
        this.MentionpageNumber--;
      },

      //Total number of pages
      MentionpageCount() {
        return Math.ceil(this.total_of_mentions / this.total_of_mentions);
      },
      //Return the start range of the paginated results
      MentionstartResults() {
        return this.MentionpageNumber * this.mention_page_size + 1;
      },

      //Return the end range of the paginated results
      MentionendResults() {
        let resultsOnPage = (this.MentionpageNumber + 1) * this.mention_page_size;
        if (resultsOnPage <= this.total_of_mentions) {
          return resultsOnPage;
        }
        return this.total_of_mentions;
      },
      //Link to navigate to page
      MentionviewPage(index) {
        this.MentionpageNumber = index;
      },
    };
}
