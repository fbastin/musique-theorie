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
    \key a \minor
    \once \override Staff.HorizontalBracketText.text = "naturelle"
    a\startGroup b c' d' e' f' g' a'\stopGroup
    \bar "" \break
    \once \override Staff.HorizontalBracketText.text = "harmonique"
    a\startGroup b c' d' e' f' gis' a'\stopGroup
    \bar "" \break
    \once \override Staff.HorizontalBracketText.text = "mélodique"
    a\startGroup b c' d' e' fis' gis' a'\stopGroup
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
