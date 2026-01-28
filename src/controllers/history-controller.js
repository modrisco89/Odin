import { db } from "../models/db.js";

export const historyController = {
  index: {
    handler: async function (request, h) {
      const opinions = await db.infoStore.getAllinfos(); 
      const viewData = {
        title: "Odin's History",
        Info: opinions,
      };
      return h.view("history-view", viewData);
    },
  },

    clearLog: {
    handler: async function (request, h) {
      await db.infoStore.deleteAllinfos();
      return h.redirect("/history");
    },
  },
};
