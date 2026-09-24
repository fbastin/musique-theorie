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
    \clef treble
    \omit Staff.TimeSignature
    \cadenzaOn
    \key c \major
    \once \override Staff.HorizontalBracketText.text = "majeur"
    c'\startGroup d' e' f'\stopGroup
    \bar "" \break
    \once \override Staff.HorizontalBracketText.text = "mineur"
    c'\startGroup d' ees' f'\stopGroup
    \bar "" \break
    \once \override Staff.HorizontalBracketText.text = "phrygien"
    c'\startGroup des' ees' f'\stopGroup
    \bar "" \break
    \once \override Staff.HorizontalBracketText.text = "harmonique"
    c'\startGroup des' e' f'\stopGroup
    \bar "" \break
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
