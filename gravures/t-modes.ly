\version "2.24.3"
%% Fichier produit par outils/generer_tonalites.py — ne pas modifier à la main.
\paper {
  indent = 0
  ragged-right = ##t
  top-margin = 1\mm
  bottom-margin = 1\mm
  left-margin = 1\mm
  right-margin = 1\mm
  oddHeaderMarkup = ##f
  evenHeaderMarkup = ##f
  oddFooterMarkup = ##f
  evenFooterMarkup = ##f
  bookTitleMarkup = ##f
  scoreTitleMarkup = ##f
}
\score {
  \new Staff \with {
    \consists "Horizontal_bracket_engraver"
    \override HorizontalBracket.direction = #DOWN
    \override HorizontalBracketText.font-size = #-3
    \override HorizontalBracketText.font-shape = #'italic
  } {
    %% Sans barres de mesure, une altération reste en vigueur jusqu'à la fin de
    %% la figure : le ré bémol du tétracorde phrygien n'était pas réimprimé sur
    %% la ligne du tétracorde harmonique, qui se lisait donc « do ré mi fa » —
    %% l'orthographe du tétracorde majeur. Même effet sur la mineure mélodique,
    %% dont le sol dièse disparaissait et qui se lisait en mode dorien.
    %% `forget` réimprime chaque altération par rapport à l'armure, sans
    %% mémoire de ce qui précède : chaque ligne se lit alors seule.
    \accidentalStyle forget
    \clef treble
    \omit Staff.TimeSignature
    \cadenzaOn
    \key c \major
    \once \override Staff.HorizontalBracketText.text = "majeur"
    c'^\markup \small \bold "do ionien"\startGroup d' e' f'\stopGroup
    \once \override Staff.HorizontalBracketText.text = "majeur"
    g'\startGroup a' b' c''\stopGroup
    \bar "||"
    \once \override Staff.HorizontalBracketText.text = "mineur"
    d'^\markup \small \bold "ré dorien"\startGroup e' f' g'\stopGroup
    \once \override Staff.HorizontalBracketText.text = "mineur"
    a'\startGroup b' c'' d''\stopGroup
    \bar "" \break
    \once \override Staff.HorizontalBracketText.text = "phrygien"
    e'^\markup \small \bold "mi phrygien"\startGroup f' g' a'\stopGroup
    \once \override Staff.HorizontalBracketText.text = "phrygien"
    b'\startGroup c'' d'' e''\stopGroup
    \bar "||"
    \once \override Staff.HorizontalBracketText.text = "lydien"
    f'^\markup \small \bold "fa lydien"\startGroup g' a' b'\stopGroup
    \once \override Staff.HorizontalBracketText.text = "majeur"
    c''\startGroup d'' e'' f''\stopGroup
    \bar "" \break
    \once \override Staff.HorizontalBracketText.text = "majeur"
    g'^\markup \small \bold "sol mixolydien"\startGroup a' b' c''\stopGroup
    \once \override Staff.HorizontalBracketText.text = "mineur"
    d''\startGroup e'' f'' g''\stopGroup
    \bar "||"
    \once \override Staff.HorizontalBracketText.text = "mineur"
    a^\markup \small \bold "la éolien"\startGroup b c' d'\stopGroup
    \once \override Staff.HorizontalBracketText.text = "phrygien"
    e'\startGroup f' g' a'\stopGroup
    \bar "" \break
    \once \override Staff.HorizontalBracketText.text = "phrygien"
    b^\markup \small \bold "si locrien"\startGroup c' d' e'\stopGroup
    \once \override Staff.HorizontalBracketText.text = "lydien"
    f'\startGroup g' a' b'\stopGroup
    \bar "|."
  }
  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/2)
      \override SpacingSpanner.spacing-increment = #2.2
    }
  }
}
