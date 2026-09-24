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
  <<
    \new Staff {
      \clef treble \key c \major \omit Staff.TimeSignature \cadenzaOn
      c' d' e' f' g' a' b' c''
      \bar "|."
    }
    \addlyrics { to -- ni -- que sus -- to -- ni -- que mé -- diante sous -- do -- mi -- nante do -- mi -- nante sus -- do -- mi -- nante sen -- si -- ble to -- ni -- que }
  >>
  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/2)
      \override SpacingSpanner.spacing-increment = #2.2
    }
    \context { \Lyrics \override LyricText.font-size = #-2.5 }
  }
}
