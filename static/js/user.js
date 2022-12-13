
function Users() {
    return {
      search: "",
      pageNumber: 0,
      sortCol:null,
      size: 5,
      total: "",
      myForData: users,
      options:['5','10','25','50','All'],
      light : true,
      init(){
        this.light = localStorage.getItem("light") == 'true'
      },
      get users() {
        const start = this.pageNumber * this.size,
          end = start + this.size;
        if (this.search === "") {
          this.total = this.myForData.length;
          return this.myForData.slice(start, end);
        }

        //Return the total results of the filters
        this.total = this.myForData.filter((item) => {
          return (item.first_name.toLowerCase().includes(this.search.toLowerCase()) || item.email.toLowerCase().includes(this.search.toLowerCase()) || item.role__name.toLowerCase().includes(this.search.toLowerCase()))
        }).length;

        //Return the filtered data
        return this.myForData
          .filter((item) => {
                 return item.first_name.toLowerCase().includes(this.search.toLowerCase()) || item.email.toLowerCase().includes(this.search.toLowerCase()) || item.role__name.toLowerCase().includes(this.search.toLowerCase())
          })
          .slice(start, end);
      },

      sort(col) {
          if(this.sortCol === col) this.sortAsc = !this.sortAsc;
          this.sortCol = col;
          this.myForData.sort((a, b) => {
            if(a[this.sortCol] < b[this.sortCol]) return this.sortAsc?1:-1;
            if(a[this.sortCol] > b[this.sortCol]) return this.sortAsc?-1:1;
            return 0;
          });
       },

      changeSize(page_size){
       page_size != 'All' ? this.size = parseInt(page_size) : this.size = this.myForData.length
       this.users
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
