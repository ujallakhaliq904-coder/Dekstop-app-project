import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import tkinter as tk
from tkinter import ttk

class Styles:
    LIGHT_THEME = {
        'bg': '#f0f2f5',
        'fg': '#1a1a1a',
        'frame_bg': '#ffffff',
        'accent': '#1890ff',
        'accent_hover': '#40a9ff',
        'error': '#ff4d4f',
        'success': '#52c41a'
    }

    DARK_THEME = {
        'bg': '#141414',
        'fg': '#ffffff',
        'frame_bg': '#1f1f1f',
        'accent': '#177ddc',
        'accent_hover': '#389e0d',
        'error': '#a61d24',
        'success': '#49aa19'
    }

    FONTS = {
        'h1': ('Segoe UI', 24, 'bold'),
        'h2': ('Segoe UI', 18, 'bold'),
        'body': ('Segoe UI', 12),
        'small': ('Segoe UI', 10)
    }

    @classmethod
    def apply_theme(cls, root, theme_name='light'):
        theme = cls.DARK_THEME if theme_name == 'dark' else cls.LIGHT_THEME
        
        style = ttk.Style(root)
        
        # Configure root colors
        root.configure(bg=theme['bg'])
        
        # Configure common styles
        style.configure('TFrame', background=theme['bg'])
        style.configure('Card.TFrame', background=theme['frame_bg'], borderwidth=1, relief='solid')
        
        style.configure('TLabel', background=theme['bg'], foreground=theme['fg'], font=cls.FONTS['body'])
        style.configure('Card.TLabel', background=theme['frame_bg'], foreground=theme['fg'])
        style.configure('Header.TLabel', font=cls.FONTS['h1'], background=theme['bg'], foreground=theme['fg'])
        style.configure('SubHeader.TLabel', font=cls.FONTS['h2'], background=theme['bg'], foreground=theme['fg'])
        style.configure('Error.TLabel', foreground=theme['error'], background=theme['bg'])
        
        style.configure('TButton', font=cls.FONTS['body'], padding=5)
        style.map('Accent.TButton',
            background=[('active', theme['accent_hover']), ('!active', theme['accent'])],
            foreground=[('!active', 'white')]
        )
        
        style.configure('TEntry', fieldbackground=theme['frame_bg'], foreground=theme['fg'])
        style.configure('TCombobox', fieldbackground=theme['frame_bg'], foreground=theme['fg'])
        
        # Treeview styling
        style.configure('Treeview', 
            background=theme['frame_bg'], 
            fieldbackground=theme['frame_bg'], 
            foreground=theme['fg'],
            rowheight=30,
            font=cls.FONTS['body']
        )
        style.configure('Treeview.Heading', font=cls.FONTS['body'], background=theme['bg'])
        style.map('Treeview', background=[('selected', theme['accent'])], foreground=[('selected', 'white')])

        return theme
