package com.linkmanager.linkplugin;

import org.bukkit.entity.Player;
import org.bukkit.event.EventHandler;
import org.bukkit.event.Listener;
import org.bukkit.event.player.PlayerJoinEvent;

import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.format.NamedTextColor;
import net.kyori.adventure.text.format.TextDecoration;

import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Random;

public class JoinListener implements Listener {

    private final LinkPlugin plugin;

    public JoinListener(LinkPlugin plugin) {
        this.plugin = plugin;
    }

    @EventHandler
    public void onJoin(PlayerJoinEvent event) {
        Player p = event.getPlayer();

        if (plugin.database.getConnection() == null) {
            Component kickMessage = Component.text("The verification system is currently offline.")
                    .color(NamedTextColor.RED)
                    .decorate(TextDecoration.BOLD)
                    .append(Component.newline())
                    .append(Component.text("Please try again later.")
                    .color(NamedTextColor.GRAY));

            p.kick(kickMessage);
            return;
        }

        String code = generateCode();

        while (codeExists(code)) {
            code = generateCode();
        }

        saveCode(code, p);

        Component kickMessage = Component.text("Your verification code:")
                .color(NamedTextColor.GREEN)
                .decorate(TextDecoration.BOLD)
                .append(Component.newline())
                .append(
                    Component.text(code)
                    .color(NamedTextColor.YELLOW)
                    .decorate(TextDecoration.BOLD)
                );

        p.kick(kickMessage);
    }

    private String generateCode() {
        Random r = new Random();
        int num = r.nextInt(900000) + 100000;
        return String.valueOf(num);
    }

    private boolean codeExists(String code) {
        try {
            PreparedStatement st = plugin.database.getConnection()
                    .prepareStatement("SELECT code FROM verify_codes WHERE code=?");
            st.setString(1, code);
            ResultSet rs = st.executeQuery();
            return rs.next();
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return true;
    }

    private void saveCode(String code, Player p) {
        try {
            PreparedStatement st = plugin.database.getConnection()
                    .prepareStatement("INSERT INTO verify_codes (code, username, uuid) VALUES (?, ?, ?)");
            st.setString(1, code);
            st.setString(2, p.getName());
            st.setString(3, p.getUniqueId().toString());
            st.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
