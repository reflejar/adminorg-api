// APEX React Template Config File
//-------------------------------

// You can customize the theme with the help of this file

//Template config options
const templateConfig = {
   layoutColor: 'layout-light', // Options: layout-dark, layout-light - Set layout-dark for dark mode and layout-light for light.
   // fixedNavbar: true, // Options: true, false - Set true for fixed navbar.
   sidebar: {
      collapsed: true, // Options: true, false | Set false to keep the sidebar open / set it to true for collapsed sidebar by default
      size: 'sidebar-md', // Options: 'sidebar-lg', 'sidebar-md', 'sidebar-sm'
      backgroundColor: "purple-bliss",
      // Gradient Options: 'pomegranate', 'king-yna', 'ibiza-sunset', 'flickr', 'purple-bliss', 'man-of-steel', 'purple-love'
      // Solid Options: 'black', 'white', 'blue', 'purple', 'red', 'orange', 'navy-blue'
      backgroundImage: false, // Options: true, false | Set true to show background image
   },
   buyNow: false, // Options: true, false - To show floating buy now button.
};


export default templateConfig;