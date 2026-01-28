import { aboutController } from "./controllers/about-controller.js";
import { accountsController } from "./controllers/accounts-controller.js";
import { dashboardController } from "./controllers/dashboard-controller.js";
import { venueController } from "./controllers/venue-controller.js";
import { infoController } from "./controllers/info-controller.js";
import { historyController } from "./controllers/history-controller.js";

export const webRoutes = [
  { method: "GET", path: "/", config: accountsController.index },
  { method: "GET", path: "/signup", config: accountsController.showSignup },
  { method: "GET", path: "/login", config: accountsController.showLogin },
  { method: "GET", path: "/logout", config: accountsController.logout },
  { method: "GET", path: "/settings", config: accountsController.settingsView},
  { method: "POST", path: "/update", config: accountsController.update},
  { method: "POST", path: "/register", config: accountsController.signup },
  { method: "POST", path: "/authenticate", config: accountsController.login },

  { method: "GET", path: "/deleteuser/{userid}", config: accountsController.deleteUser },
 { method: "POST", path: "/updateuser/{userid}", config: accountsController.updateUser },

  { method: "GET", path: "/about", config: aboutController.index },
  { method: "GET", path: "/history", config: historyController.index },
  { method: "GET", path: "/history/clearlog", config: historyController.clearLog },
  { method: "GET", path: "/dashboard", config: dashboardController.index },
  { method: "POST", path: "/dashboard/addvenue", config: dashboardController.addvenue },
  { method: "GET", path: "/dashboard/deletevenue/{id}", config: dashboardController.deletevenue },

  { method: "GET", path: "/venue/{id}", config: venueController.index },
  { method: "POST", path: "/venue/{id}/addinfo", config: venueController.addinfo },
  { method: "GET", path: "/venue/{id}/deleteinfo/{infoid}", config: venueController.deleteinfo },

  { method: "GET", path: "/info/{id}/editinfo/{infoid}", config: infoController.index },
  { method: "POST", path: "/info/{id}/updateinfo/{infoid}", config: infoController.update },

  { method: "GET", path: "/dashboard/clearlog", config: dashboardController.clearLog },
];
