\version "2.24.3"
%% Fichier produit par outils/generer_valeurs.py — ne pas modifier à la main.
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
  \new StaffGroup <<
    \new Staff \with { instrumentName = \markup \small \italic "régulier" } {
      \clef treble \omit Staff.TimeSignature \cadenzaOn \autoBeamOff \tupletUp
      \textMark \markup \small \italic "triolet de croches" a'8[ a'8] \bar "|" \textMark \markup \small \italic "triolet de noires" a'4 a'4 \bar "|" \textMark \markup \small \italic "triolet de doubles" a'16[ a'16] \bar "|" \textMark \markup \small \italic "sextolet" a'16[ a'16 a'16 a'16]
      \bar "|."
    }
    \new Staff \with { instrumentName = \markup \small \italic "irrégulier" } {
      \clef treble \omit Staff.TimeSignature \cadenzaOn \autoBeamOff \tupletUp
      \tuplet 3/2 { a'8[ a'8 a'8] } \bar "|" \tuplet 3/2 { a'4 a'4 a'4 } \bar "|" \tuplet 3/2 { a'16[ a'16 a'16] } \bar "|" \tuplet 6/4 { a'16[ a'16 a'16 a'16 a'16 a'16] }
      \bar "|."
    }
  >>
  \layout {
    indent = 18\mm line-width = 300\mm
    \context { \Score \override SpacingSpanner.spacing-increment = #1.6 \markLengthOn \override TextMark.self-alignment-X = #LEFT }
  }
}
