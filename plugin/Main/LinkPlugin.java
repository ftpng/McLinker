package plugin.Main;

public class LinkPlugin {
    
}
package com.linkmanager.linkplugin;

import org.bukkit.plugin.java.JavaPlugin;

public class LinkPlugin extends JavaPlugin {

    public Database database = new Database();

    @Override
    public void onEnable() {

        saveDefaultConfig();

        String host = getConfig().getString("database.host");
        int port = getConfig().getInt("database.port");
        String db = getConfig().getString("database.database");
        String user = getConfig().getString("database.username");
        String pass = getConfig().getString("database.password");

        try {
            database.connect(host, port, db, user, pass);
            getLogger().info("Connected to MySQL!");
        } catch (Exception e) {
            getLogger().severe("Failed to connect to MySQL!");
            e.printStackTrace();
        }

        getServer().getPluginManager().registerEvents(new JoinListener(this), this);
    }

    @Override
    public void onDisable() {
        getLogger().info("LinkPlugin disabled.");
    }
}