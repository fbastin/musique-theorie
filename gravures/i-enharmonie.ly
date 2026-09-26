\version "2.24.3"
%% Fichier produit par outils/generer.py — ne pas modifier à la main.
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
    \once \override Staff.HorizontalBracketText.text = "2de aug."
    f'\startGroup  gis'\stopGroup
    \once \override Staff.HorizontalBracketText.text = "3ce m"
    f'\startGroup  aes'\stopGroup
    \once \override Staff.HorizontalBracketText.text = "4te aug."
    c'\startGroup  fis'\stopGroup
    \once \override Staff.HorizontalBracketText.text = "5te dim."
    c'\startGroup  ges'\stopGroup
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
